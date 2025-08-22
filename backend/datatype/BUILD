py_library(
    name="Zone",
    srcs=["Zone.py"],
    deps=[":IrrigationInfo", "//backend/hw_io:gpio", ":DbLogUtils", "//backend/dao:PersistentLogDAO"],
    visibility=["//backend:__subpackages__"],
)

py_library(
    name="IrrigationInfo",
    srcs=["IrrigationInfo.py"],
    visibility=["//backend:__subpackages__"],
)

py_library(name="Log", srcs=["Log.py"], visibility=["//backend:__subpackages__"])
py_library(name="DbLogUtils", srcs=["DbLogUtils.py"], visibility=["//backend:__subpackages__"])

py_test(
    name="TestZone",
    srcs=["TestZone.py"],
    deps=[":Zone"],
)
