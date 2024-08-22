import lupa

with lupa.allow_lua_module_loading():
    from lupa import lua51

lua = lua51.LuaRuntime(encoding="ISO-8859-1")

lua.execute("LibSerialize = require('lib.LibSerialize')")

# !PTL1!Jr)uZP8sm3ulQKulUednY4dLAffKFrLeCjfLzEPxG)ohA2oIdG7zfvUr5BUrLDu5wrKr6Rpv5RVzvsu(Mvu(wv5ajDpPCJYOCJQCOQ2tNYnk3D0OStTYlbYMui5elj10ZVOkVaJxkeq8DgkFad
importString = "Jr)uZP8sm3ulQKulUednY4dLAffKFrLeCjfLzEPxG)ohA2oIdG7zfvUr5BUrLDu5wrKr6Rpv5RVzvsu(Mvu(wv5ajDpPCJYOCJQCOQ2tNYnk3D0OStTYlbYMui5elj10ZVOkVaJxkeq8DgkFad"


LibDeflate = lua.require("lib.LibDeflate")
LibSerialize = lua.require("lib.LibSerialize")

decoded = LibDeflate.DecodeForPrint(LibDeflate, importString)
decompressed, _ = LibDeflate.DecompressDeflate(LibDeflate, decoded)
success, data = LibSerialize.Deserialize(LibSerialize, decompressed)

print(decompressed)
print(dict(data))
print(dict(data[1]))
