py_library(
    name = "IrrigationInfoDAO",
    srcs = ["irrigation_info_dao.py"],
    visibility = ["//backend/dao:__subpackages__"],
    deps = [
        "//backend/datatype:IrrigationInfo",
        "//backend/datatype:Zone",
        "//backend/db:SqlLite",
    ],
)

py_library(
    name = "ZoneDAO",
    srcs = ["zone_dao.py"],
    visibility = ["//backend:__subpackages__"],
    deps = [
        "//backend/dao:IrrigationInfoDAO",
        "//backend/dao:PersistentLogDAO",
        "//backend/datatype:IrrigationInfo",
        "//backend/datatype:Zone",
        "//backend/db:SqlLite",
    ],
)

py_library(
    name = "PersistentLogDAO",
    srcs = ["persistent_log_dao.py"],
    visibility = ["//backend:__subpackages__"],
    deps = [
        "//backend/datatype:Log",
        "//backend/db:SqlLite",
    ],
)
