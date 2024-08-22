from typing import NamedTuple

import lupa

with lupa.allow_lua_module_loading():
    from lupa import lua51

lua = lua51.LuaRuntime(encoding="ISO-8859-1")

LibDeflate = lua.require("lib.LibDeflate")
LibSerialize = lua.require("lib.LibSerialize")


class LoadoutData(NamedTuple):
    name: str
    loadouts: dict[str, str]


class CategoryCreator:
    def _create_loadout_table(self, name: str, loadout: str):
        return lua.table(name=name, exportString=loadout)

    def _create_export_table(self, category_name: str, loadouts: dict):
        key = category_name.lower()
        loadout_tables = []
        for loadout_name, export_string in loadouts.items():
            loadout_tables.append(
                self._create_loadout_table(loadout_name, export_string)
            )
        return lua.table(
            *loadout_tables,
            key=key,
            name=category_name,
        )

    def create_export_string(self, loadout_data: LoadoutData):
        export_table = self._create_export_table(
            loadout_data.name, loadout_data.loadouts
        )

        serialized = LibSerialize.Serialize(LibSerialize, export_table)
        compressed, _ = LibDeflate.CompressDeflate(LibDeflate, serialized)
        encode = LibDeflate.EncodeForPrint(LibDeflate, compressed)
        return f"!PTL1!{encode}"
