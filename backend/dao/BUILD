py_library(
    name = "IrrigationInfoDAO",
    srcs = ["IrrigationInfoDAO.py"],
    deps = [
        "//backend/db:SqlLite",
        "//backend/datatype:IrrigationInfo",
        "//backend/datatype:Zone",
        ],
    visibility = ["//backend/dao:__subpackages__"],
)

py_library(
    name = "ZoneDAO",
    srcs = ["ZoneDAO.py"],
    deps = [
        "//backend/db:SqlLite",
        "//backend/datatype:Zone",
        "//backend/datatype:IrrigationInfo",
        "//backend/dao:IrrigationInfoDAO",
        "//backend/dao:PersistentLogDAO",],
    visibility = ["//backend:__subpackages__"],)

py_library(
    name = "PersistentLogDAO",
    srcs = ["PersistentLogDAO.py"],
    deps = [
        "//backend/db:SqlLite",
        "//backend/datatype:Log",
        ],
        visibility = ["//backend:__subpackages__"],
        )

