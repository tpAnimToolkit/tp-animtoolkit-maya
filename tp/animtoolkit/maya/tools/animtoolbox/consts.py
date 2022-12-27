ROTATE_ORDERS = ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']
SELECT_OPTIONS = ['Under Selected Hierarchy', 'Scene (All)', 'Within Selected']

CHANGE_ROTATE_ORDER_COMBO_TOOLTIP = """
Change Rotation Order - Changes the XYZ rotation order on selected transforms.
If objects have keyframes, will change each key to compensate for the correct rotation.
"""
SELECT_ANIMATED_NODES_TOOLTIP = """
Select all animated nodes filtered by the dropdown menu.
"""
SET_KEY_ALL_CHANNELS_TOOLTIP = """
Set key on all attributes, but if any channel box attributes are selected, then key only those channels.
Hotkey: s
"""
SET_KEY_CHANNELS_TOOLTIP = """
Sets a key on all attributes ignoring any channel box selection.
Hotkey: shift + s
"""
ANIM_ON_HOLD_TOOLTIP = """
Places the timeline between two keys and run. The first key will be copied to the second key with flat tangents.
Hotkey: alt + a
"""
DELETE_CURRENT_FRAME_TOOLTIP = """
Deletes keys at the current time or the selected timeline range.
Hotkey: ctrl + shift + v
"""
TOGGLE_VIS_TOOLTIP = """
Keys and inverts the visibility of the selected objects
Hotkey: Ctrl + Shift + Alt + v
"""
RESET_ATTRS_TOOLTIP = """
Resets the selected object/s attributes to default values.
Hotkey: Ctrl + Shift + Alt + s
"""
TOGGLE_CURVE_VISIBILITY_TOOLTIP = """
Toggles the visibility of controls and curves
Hotkey: d (tap)
"""