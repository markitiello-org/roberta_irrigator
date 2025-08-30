py_library(
    name = "Zone",
    srcs = ["zone.py"],
    visibility = ["//backend:__subpackages__"],
    deps = [
        ":IrrigationInfo",
        "//backend/dao:PersistentLogDAO",
        "//backend/hw_io:gpio",
    ],
)

py_library(
    name = "IrrigationInfo",
    srcs = ["irrigation_info.py"],
    visibility = ["//backend:__subpackages__"],
)

py_library(
    name = "Log",
    srcs = ["log.py"],
    visibility = ["//backend:__subpackages__"],
)
