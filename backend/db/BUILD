py_test(
    name = "TestSqlLite",
    srcs = ["TestSqlLite.py"],
    deps = [":SqlLite"]
)

py_library(
    name = "SqlLite",
    srcs = ["SqlLite.py"],
    deps = ["//backend/datatype:Log"],
    visibility = ["//backend:__subpackages__"]
)