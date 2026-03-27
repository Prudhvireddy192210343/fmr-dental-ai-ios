
# Clinical feature configuration

FEATURE_COLUMNS = [
    "F001_Age",
    "F002_Missing_Teeth_Count",
    "F003_Periodontal_Severity",
    "F004_Bone_Loss_Percentage",
    "F005_Caries_Risk",
    "F006_Pulpal_Involvement",
    "F007_Occlusal_Stability",
    "F008_Vertical_Dimension_Loss",
    "F009_TMJ_Disorder",
    "F010_Systemic_Risk",
    "F011_Implant_Indicated",
    "F012_Esthetic_Demand"
]

IMAGE_CLASSES = {
    0: "Normal",
    1: "Caries",
    2: "Bone Loss",
    3: "Periapical Lesion"
}
