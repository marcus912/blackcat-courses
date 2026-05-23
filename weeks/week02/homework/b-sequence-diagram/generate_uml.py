"""
Generate a StarUML 1 (.uml / XPD) sequence diagram for the pygame collision sim.

Why a generator? StarUML 1's XPD format requires GUIDs everywhere with
denormalized cross-references (each ClassifierRole tracks its own Sender/Receiver
client message lists). Writing it by hand for 12 lifelines and ~20 messages is
infeasible — this script builds it deterministically.

Caveats:
- StarUML 1 sequence diagrams predate UML 2.0 combined fragments.
  loop / alt / opt blocks from the Mermaid version are FLATTENED here:
  iteration is captured by adding "[loop ...]" / "[alt ...]" prefixes to
  message names. The reader gets the order; it just won't render as boxes.
- Layout: lifelines positioned at fixed X-step, messages at fixed Y-step.

Usage:
    python3 generate_uml.py > sequence.uml
"""

import base64
import os
import sys
from pathlib import Path


# ---------- GUID helper ----------
# StarUML 1 GUIDs are base64 of 16 random bytes, ending in "AA" (the trailing
# byte is always 0x00 in the originals — we replicate that to be safe).
_guid_counter = 0


def make_guid() -> str:
    """Deterministic, sequential GUIDs so re-runs produce stable diffs."""
    global _guid_counter
    _guid_counter += 1
    raw = _guid_counter.to_bytes(15, "big") + b"\x00"
    # Pad to 16 bytes total, base64 produces 24 chars; replace last 2 with "AA"
    b64 = base64.b64encode(raw).decode("ascii")
    return b64[:-2] + "AA"


# ---------- Diagram spec ----------
# Order matters — left to right on the diagram.
LIFELINES = [
    "User",
    "MainLoop",
    "Clock",
    "Window",
    "Mouse",
    "Event",
    "calculate_movement",
    "handle_collisions",
    "draw_collidables",
    "draw_current_object",
    "pygame_draw",
    "collidables",
]

# Each message: (sender, receiver, label)
# Order = top-to-bottom on the diagram.
# loop / alt / opt prefixes encode the structure that StarUML 1 can't render.
MESSAGES = [
    ("MainLoop", "Clock", "[loop frame] tick(FPS)"),
    ("MainLoop", "Window", "fill(black)"),
    ("MainLoop", "Mouse", "get_pos()"),
    ("Mouse", "MainLoop", "return mouse_pos"),
    ("MainLoop", "Event", "get()"),
    ("Event", "MainLoop", "return events[]"),
    ("MainLoop", "MainLoop", "[loop event] dispatch by type"),
    ("User", "MainLoop", "[alt MOUSEBUTTONDOWN] left click"),
    ("MainLoop", "collidables", "append(new_obj)"),
    ("MainLoop", "collidables", "[alt KEYDOWN c] clear()"),
    ("MainLoop", "calculate_movement", "calculate_movement()"),
    ("calculate_movement", "collidables", "[loop o,other] update other.velocity"),
    ("calculate_movement", "pygame_draw", "[opt draw_attractions] line(o.pos,other.pos)"),
    ("MainLoop", "handle_collisions", "handle_collisions()"),
    ("handle_collisions", "collidables", "[loop pairs] absorb smaller into bigger"),
    ("handle_collisions", "collidables", "collidables[:] = survivors"),
    ("MainLoop", "draw_collidables", "draw_collidables()"),
    ("draw_collidables", "collidables", "[loop obj] obj.pos += obj.velocity"),
    ("draw_collidables", "pygame_draw", "circle(window,colour,pos,radius)"),
    ("MainLoop", "draw_current_object", "draw_current_object()"),
    ("draw_current_object", "draw_current_object", "[alt radius out of (1,20)] expansion *= -1"),
    ("draw_current_object", "pygame_draw", "circle(window,red,pos,radius)"),
    ("MainLoop", "Window", "display.update()"),
]


# ---------- Layout constants ----------
LIFELINE_TOP = 36
LIFELINE_HEIGHT = 800
LIFELINE_WIDTH = 130
LIFELINE_X_START = 40
LIFELINE_X_STEP = 160

MESSAGE_TOP = 100
MESSAGE_Y_STEP = 28


def lifeline_x_center(idx: int) -> int:
    return LIFELINE_X_START + idx * LIFELINE_X_STEP + LIFELINE_WIDTH // 2


# ---------- Pre-allocate GUIDs ----------
g_project = make_guid()
g_use_case_model = make_guid()
g_use_case_diag = make_guid()
g_use_case_diag_view = make_guid()
g_analysis_model = make_guid()
g_class_diag_a = make_guid()
g_class_diag_a_view = make_guid()
g_design_model = make_guid()
g_class_diag_d = make_guid()
g_class_diag_d_view = make_guid()
g_impl_model = make_guid()
g_comp_diag = make_guid()
g_comp_diag_view = make_guid()
g_deploy_model = make_guid()
g_deploy_diag = make_guid()
g_deploy_diag_view = make_guid()
g_seq_model = make_guid()
g_collab = make_guid()
g_interaction = make_guid()
g_seq_diag = make_guid()
g_seq_diag_view = make_guid()

# ClassifierRole GUIDs and their primary view GUIDs
role_guid = {name: make_guid() for name in LIFELINES}
role_view_guid = {name: make_guid() for name in LIFELINES}
lifeline_view_guid = {name: make_guid() for name in LIFELINES}

# Message GUIDs and their view GUIDs
msg_data = []
for sender, receiver, label in MESSAGES:
    msg_data.append({
        "sender": sender,
        "receiver": receiver,
        "label": label,
        "guid": make_guid(),
        "action_guid": make_guid(),
        "view_guid": make_guid(),
        "namelabel_guid": make_guid(),
        "stereo_guid": make_guid(),
        "prop_guid": make_guid(),
        "activation_guid": make_guid(),
    })

# AssociationRole — one per (sender, receiver) ordered pair that has messages.
assoc_pairs = {}
for m in msg_data:
    if m["sender"] == m["receiver"]:
        continue
    key = (m["sender"], m["receiver"])
    assoc_pairs.setdefault(key, []).append(m["guid"])

assoc_data = []
for (s, r), msg_guids in assoc_pairs.items():
    assoc_data.append({
        "sender": s,
        "receiver": r,
        "guid": make_guid(),
        "end_sender_guid": make_guid(),
        "end_receiver_guid": make_guid(),
        "messages": msg_guids,
    })


# ---------- XML emitter ----------
out = []


def w(line: str = "") -> None:
    out.append(line)


def obj_open(name: str, type_: str, guid: str) -> None:
    w(f'<XPD:OBJ name="{name}" type="{type_}" guid="{guid}">')


def obj_close() -> None:
    w("</XPD:OBJ>")


def attr(name: str, type_: str, value: str) -> None:
    w(f'<XPD:ATTR name="{name}" type="{type_}">{value}</XPD:ATTR>')


def ref(name: str, value: str) -> None:
    w(f'<XPD:REF name="{name}">{value}</XPD:REF>')


def xml_escape(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


# ---------- Header ----------
w('<?xml version="1.0" encoding="UTF-8"?>')
w('<XPD:PROJECT xmlns:XPD="http://www.staruml.com" version="1">')
w("<XPD:HEADER>")
w("<XPD:SUBUNITS></XPD:SUBUNITS>")
w("<XPD:PROFILES>")
w("<XPD:PROFILE>UMLStandard</XPD:PROFILE>")
w("</XPD:PROFILES>")
w("</XPD:HEADER>")
w("<XPD:BODY>")

# DocumentElement / Project
obj_open("DocumentElement", "UMLProject", g_project)
attr("Title", "string", "PygameCollisionSequence")
attr("#OwnedElements", "integer", "6")

# Stub use case / analysis / design / impl / deploy models (StarUML expects them)
def stub_model(idx: int, name: str, stereo: str, model_guid: str,
               diag_type: str, diag_guid: str, diag_view_guid: str,
               diag_view_type: str) -> None:
    obj_open(f"OwnedElements[{idx}]", "UMLModel", model_guid)
    attr("Name", "string", name)
    attr("StereotypeProfile", "string", "UMLStandard")
    attr("StereotypeName", "string", stereo)
    ref("Namespace", g_project)
    attr("#OwnedDiagrams", "integer", "1")
    obj_open("OwnedDiagrams[0]", diag_type, diag_guid)
    attr("Name", "string", "Main")
    ref("DiagramOwner", model_guid)
    obj_open("DiagramView", diag_view_type, diag_view_guid)
    ref("Diagram", diag_guid)
    obj_close()
    obj_close()
    obj_close()


stub_model(0, "Use Case Model", "useCaseModel", g_use_case_model,
           "UMLUseCaseDiagram", g_use_case_diag, g_use_case_diag_view,
           "UMLUseCaseDiagramView")
stub_model(1, "Analysis Model", "analysisModel", g_analysis_model,
           "UMLClassDiagram", g_class_diag_a, g_class_diag_a_view,
           "UMLClassDiagramView")
stub_model(2, "Design Model", "designModel", g_design_model,
           "UMLClassDiagram", g_class_diag_d, g_class_diag_d_view,
           "UMLClassDiagramView")
stub_model(3, "Implementation Model", "implementationModel", g_impl_model,
           "UMLComponentDiagram", g_comp_diag, g_comp_diag_view,
           "UMLComponentDiagramView")
stub_model(4, "Deployment Model", "deploymentModel", g_deploy_model,
           "UMLDeploymentDiagram", g_deploy_diag, g_deploy_diag_view,
           "UMLDeploymentDiagramView")

# ---- Sequence model (the real content) ----
obj_open("OwnedElements[5]", "UMLModel", g_seq_model)
attr("Name", "string", "sequence")
ref("Namespace", g_project)
attr("#OwnedCollaborations", "integer", "1")

obj_open("OwnedCollaborations[0]", "UMLCollaboration", g_collab)
attr("Name", "string", "PygameCollisionFrame")
ref("RepresentedClassifier", g_seq_model)

# OwnedElements: ClassifierRoles + AssociationRoles
total_owned = len(LIFELINES) + len(assoc_data)
attr("#OwnedElements", "integer", str(total_owned))

# Build sender/receiver indexes for ClassifierRoles
sender_msgs = {n: [] for n in LIFELINES}
receiver_msgs = {n: [] for n in LIFELINES}
for m in msg_data:
    sender_msgs[m["sender"]].append(m["guid"])
    if m["sender"] != m["receiver"]:
        receiver_msgs[m["receiver"]].append(m["guid"])

# Build association list per role
role_associations = {n: [] for n in LIFELINES}
for a in assoc_data:
    role_associations[a["sender"]].append(a["end_sender_guid"])
    role_associations[a["receiver"]].append(a["end_receiver_guid"])

# Emit ClassifierRoles
for i, name in enumerate(LIFELINES):
    obj_open(f"OwnedElements[{i}]", "UMLClassifierRole", role_guid[name])
    attr("Name", "string", xml_escape(name))
    ref("Namespace", g_collab)
    # Views: SeqClassifierRoleView, LifeLineView
    attr("#Views", "integer", "2")
    ref("Views[0]", role_view_guid[name])
    ref("Views[1]", lifeline_view_guid[name])
    if role_associations[name]:
        attr("#Associations", "integer", str(len(role_associations[name])))
        for k, g in enumerate(role_associations[name]):
            ref(f"Associations[{k}]", g)
    if sender_msgs[name]:
        attr("#SenderClientMessages", "integer", str(len(sender_msgs[name])))
        for k, g in enumerate(sender_msgs[name]):
            ref(f"SenderClientMessages[{k}]", g)
    if receiver_msgs[name]:
        attr("#ReceiverClientMessages", "integer", str(len(receiver_msgs[name])))
        for k, g in enumerate(receiver_msgs[name]):
            ref(f"ReceiverClientMessages[{k}]", g)
    obj_close()

# Emit AssociationRoles
for i, a in enumerate(assoc_data):
    idx = len(LIFELINES) + i
    obj_open(f"OwnedElements[{idx}]", "UMLAssociationRole", a["guid"])
    ref("Namespace", g_collab)
    attr("#Connections", "integer", "2")
    obj_open("Connections[0]", "UMLAssociationEndRole", a["end_sender_guid"])
    ref("Association", a["guid"])
    ref("Participant", role_guid[a["sender"]])
    obj_close()
    obj_open("Connections[1]", "UMLAssociationEndRole", a["end_receiver_guid"])
    ref("Association", a["guid"])
    ref("Participant", role_guid[a["receiver"]])
    obj_close()
    attr("#Messages", "integer", str(len(a["messages"])))
    for k, g in enumerate(a["messages"]):
        ref(f"Messages[{k}]", g)
    obj_close()

# ---- Interaction with the sequence diagram ----
attr("#Interactions", "integer", "1")
obj_open("Interactions[0]", "UMLInteraction", g_interaction)
attr("Name", "string", "OneFrame")
ref("Context", g_collab)
attr("#OwnedDiagrams", "integer", "1")

obj_open("OwnedDiagrams[0]", "UMLSequenceRoleDiagram", g_seq_diag)
attr("Name", "string", "PygameCollisionSequence")
ref("DiagramOwner", g_interaction)

# DiagramView with all OwnedViews
obj_open("DiagramView", "UMLSequenceRoleDiagramView", g_seq_diag_view)
ref("Diagram", g_seq_diag)

# OwnedViews count: lifelines + messages
n_views = len(LIFELINES) + len(msg_data)
attr("#OwnedViews", "integer", str(n_views))

# Emit lifeline views (SeqClassifierRoleView)
for i, name in enumerate(LIFELINES):
    x = LIFELINE_X_START + i * LIFELINE_X_STEP
    obj_open(f"OwnedViews[{i}]", "UMLSeqClassifierRoleView", role_view_guid[name])
    attr("LineColor", "string", "clMaroon")
    attr("FillColor", "string", "$00B9FFFF")
    attr("Left", "integer", str(x))
    attr("Top", "integer", str(LIFELINE_TOP))
    attr("Width", "integer", str(LIFELINE_WIDTH))
    attr("Height", "integer", str(LIFELINE_HEIGHT))
    ref("Model", role_guid[name])
    # NameCompartment
    obj_open("NameCompartment", "UMLNameCompartmentView", make_guid())
    obj_open("NameLabel", "LabelView", make_guid())
    attr("FontStyle", "integer", "1")
    attr("Text", "string", "/" + xml_escape(name))
    obj_close()
    obj_open("StereotypeLabel", "LabelView", make_guid())
    attr("Visible", "boolean", "False")
    obj_close()
    obj_open("PropertyLabel", "LabelView", make_guid())
    attr("Visible", "boolean", "False")
    obj_close()
    obj_close()  # NameCompartment
    # LifeLine view
    obj_open("LifeLine", "UMLLifeLineView", lifeline_view_guid[name])
    ref("Model", role_guid[name])
    obj_close()
    obj_close()  # SeqClassifierRoleView

# Emit message views
for i, m in enumerate(msg_data):
    view_idx = len(LIFELINES) + i
    sx = lifeline_x_center(LIFELINES.index(m["sender"]))
    rx = lifeline_x_center(LIFELINES.index(m["receiver"]))
    y = MESSAGE_TOP + i * MESSAGE_Y_STEP
    if m["sender"] == m["receiver"]:
        # self-message: small loop offset
        sx_pt = sx
        rx_pt = sx + 40
    else:
        sx_pt = sx
        rx_pt = rx
    obj_open(f"OwnedViews[{view_idx}]", "UMLSeqMessageView", m["view_guid"])
    attr("LineColor", "string", "clMaroon")
    attr("FillColor", "string", "$00B9FFFF")
    attr("LineStyle", "LineStyleKind", "lsRectilinear")
    attr("Points", "Points", f"{sx_pt},{y};{rx_pt},{y}")
    ref("Model", m["guid"])
    ref("Head", lifeline_view_guid[m["receiver"]])
    ref("Tail", lifeline_view_guid[m["sender"]])
    # NameLabel
    obj_open("NameLabel", "EdgeLabelView", m["namelabel_guid"])
    attr("Alpha", "real", "1.5707963267949")
    attr("Distance", "real", "10")
    attr("Text", "string", f"{i + 1} : {xml_escape(m['label'])}")
    ref("Model", m["guid"])
    ref("HostEdge", m["view_guid"])
    obj_close()
    # StereotypeLabel
    obj_open("StereotypeLabel", "EdgeLabelView", m["stereo_guid"])
    attr("Visible", "boolean", "False")
    attr("Alpha", "real", "1.5707963267949")
    attr("Distance", "real", "25")
    ref("Model", m["guid"])
    ref("HostEdge", m["view_guid"])
    obj_close()
    # PropertyLabel
    obj_open("PropertyLabel", "EdgeLabelView", m["prop_guid"])
    attr("Visible", "boolean", "False")
    attr("Alpha", "real", "-1.5707963267949")
    attr("Distance", "real", "10")
    ref("Model", m["guid"])
    ref("HostEdge", m["view_guid"])
    obj_close()
    # Activation
    obj_open("Activation", "UMLActivationView", m["activation_guid"])
    attr("Left", "integer", str(rx_pt))
    attr("Top", "integer", str(y))
    attr("Width", "integer", "14")
    attr("Height", "integer", "20")
    obj_close()
    obj_close()  # SeqMessageView

obj_close()  # DiagramView

# Messages (model)
attr("#Messages", "integer", str(len(msg_data)))
for i, m in enumerate(msg_data):
    obj_open(f"Messages[{i}]", "UMLMessage", m["guid"])
    attr("Name", "string", xml_escape(m["label"]))
    ref("Interaction", g_interaction)
    ref("Sender", role_guid[m["sender"]])
    ref("Receiver", role_guid[m["receiver"]])
    obj_open("Action", "UMLCallAction", m["action_guid"])
    ref("Message", m["guid"])
    obj_close()
    attr("#Views", "integer", "4")
    ref("Views[0]", m["view_guid"])
    ref("Views[1]", m["namelabel_guid"])
    ref("Views[2]", m["stereo_guid"])
    ref("Views[3]", m["prop_guid"])
    obj_close()

obj_close()  # SequenceRoleDiagram
obj_close()  # Interaction

obj_close()  # Collaboration
obj_close()  # sequence model

obj_close()  # DocumentElement / Project

w("</XPD:BODY>")
w("</XPD:PROJECT>")

print("\n".join(out))
