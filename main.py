from components.config import Config
from formats.format import Format
from formats.structure import Info
from parsers.cdpp.ma import Ma, MaUtil, MaComponent, MaComponentCA
from parsers.cdpp.pal import Pal
from parsers.cdpp.val import Val
from parsers.cdpp.log import Log as CdppLog
from parsers.lopez.log import Log as LopezLog
from datetime import datetime


if __name__ == '__main__':
    cfg = Config()
    cfg.make_output_folder()

    print("Started", cfg.name, "model at", datetime.now().strftime("%H:%M:%S"))
    print("Done. Parsing ma file...")
    component_class = MaComponent if cfg.formalism == "DEVS" else MaComponentCA

    ma = Ma(component_class).parse(cfg.files)

    if cfg.formalism == "DEVS":
        print("Done. Post processing the ma file...")
        MaUtil.ma_ports_from_links(ma)

    structure = MaUtil.ma_to_structure(ma, Info(cfg.simulator, cfg.name, cfg.formalism))
    val, style, messages = None, None, None

    if cfg.formalism == "Cell-DEVS":
        print("Parsing palette file if provided...")
        style = Pal().parse(cfg.files)

        print("Done. Parsing val file if provided...")
        val = Val(structure, ma.items[1]).parse(cfg.files)

    if cfg.simulator == "CDpp":
        print("Done. Parsing log file with CDpp parser...")
        messages = CdppLog(structure, val).parse(cfg.files)

    if cfg.simulator == "Lopez":
        print("Done. Parsing log file with Lopez parser...")
        messages = LopezLog(structure).parse(cfg.files)

    if messages is None:
        raise ValueError("{} and {} is an invalid combination of simulator and formalism.".format(cfg.simulator, cfg.formalism))

    print("Done. Formatting to the DEVS WebViewer specification...")
    converted = Format(structure, messages, style)

    print("Done. Writing to {}...".format(cfg.output))
    converted.output(cfg.output)

    print("Done at", datetime.now().strftime("%H:%M:%S"), "\n")
