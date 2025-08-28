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
    srcs = ["ZoneDAO.py"],
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
    srcs = ["PersistentLogDAO.py"],
    visibility = ["//backend:__subpackages__"],
    deps = [
        "//backend/datatype:Log",
        "//backend/db:SqlLite",
    ],
)
