py_binary(
    name = "start",
    srcs = ["start.py"],
    deps = ["//backend/datatype:Zone", "//backend/datatype:Log", "//backend/db:SqlLite", "//backend/hw_io:gpio", "@pip//rpyc", "//backend/dao:ZoneDAO"],
    visibility = ["//backend:__subpackages__"], 
)

py_binary(
    name = "web_api_utils",
    srcs = ["web_api_utils.py"],
    deps = ["//backend/datatype:Zone", "//backend/datatype:Log", "//backend/db:SqlLite", "//backend/hw_io:gpio", "//backend/web_service/model:zone_web",
            "@pip//flask", "@pip//rpyc", "@pip//waitress"],
    visibility = ["//backend:__subpackages__"], 
)