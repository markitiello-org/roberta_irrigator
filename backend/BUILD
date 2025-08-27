py_binary(
    name = "start",
    srcs = ["start.py"],
    visibility = ["//backend:__subpackages__"],
    deps = [
        "//backend/dao:ZoneDAO",
        "//backend/datatype:Log",
        "//backend/datatype:Zone",
        "//backend/db:SqlLite",
        "//backend/hw_io:gpio",
        "@pip//rpyc",
    ],
)

py_binary(
    name = "web_api_utils",
    srcs = ["web_api_utils.py"],
    visibility = ["//backend:__subpackages__"],
    deps = [
        "//backend/datatype:Log",
        "//backend/datatype:Zone",
        "//backend/db:SqlLite",
        "//backend/hw_io:gpio",
        "//backend/web_service/model:zone_web",
        "@pip//flask",
        "@pip//rpyc",
        "@pip//waitress",
    ],
)
