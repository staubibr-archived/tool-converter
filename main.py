import json

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

    messages, structure, style = None, None, None

    print("Started", cfg.name, "model at", datetime.now().strftime("%H:%M:%S"))

    if cfg.simulator == "CDpp" or cfg.simulator == "Lopez":
        print("Done. Parsing ma file...")
        component_class = MaComponent if cfg.formalism == "DEVS" else MaComponentCA

        ma = Ma(component_class).parse(cfg.files)

        if cfg.formalism == "DEVS":
            print("Done. Post processing the ma file...")
            MaUtil.ma_ports_from_links(ma)

        structure = MaUtil.ma_to_structure(ma, cfg.simulator, cfg.formalism)
        val, style, messages = None, None, None

        if cfg.formalism == "Cell-DEVS":
            print("Parsing palette file if provided...")
            style = Pal().parse(cfg.files)

            print("Done. Parsing val file if provided...")
            val = Val(structure, ma[1]).parse(cfg.files)

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

    # for frame in messages:
    #     print("time: " + frame.time)
    #
    #     for message in frame:
    #         print("coords: " + ','.join(message.id) + ", values: " + ','.join(message.values))
    #
    # frame5 = messages.get_frame("5")
    #
    # print("\n 5th time frame")
    # print("time: " + frame5.time + ", number of messages: " + str(len(frame5.messages)))
    #
    # message10 = frame5.messages[10]
    #
    # print("\n 10th message of 5th time frame")
    # print("coords: " + ','.join(message10.id) + ", values: " + ','.join(message10.values))
    #
    # print("\n 10th message of 5th time frame, templated")
    # model_type = structure.model_types.get_item("CO2_model")
    # templated = model_type.template_message(message10)
    # print("coords: " + ','.join(message10.id) + ", values: " + ','.join(message10.values))
    # print("coords: " + ','.join(message10.id) + ", templated values: " + json.dumps(templated))
