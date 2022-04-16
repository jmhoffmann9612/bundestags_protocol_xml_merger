import xml.etree.ElementTree as ET
import os


def merge_xml(file_id):
    root_toc = ET.parse("1_input/toc_xml/" + file_id +
                        "-vorspann.xml").getroot()
    root_content = ET.parse("1_input/content_xml/" +
                            file_id + "-main.xml").getroot()

    wahlperiode = root_toc.find("kopfdaten").find(
        "plenarprotokoll-nummer").find("wahlperiode").text
    sitzung_nr = root_toc.find("kopfdaten").find(
        "plenarprotokoll-nummer").find("sitzungsnr").text
    sitzung_datum = root_toc.find("kopfdaten").find(
        "veranstaltungsdaten").find("datum").get("date")
    sitzung_start_uhrzeit = root_content.find(
        "sitzungsbeginn").get("sitzung-start-uhrzeit")
    sitzung_ende_uhrzeit = root_content.find(
        "sitzungsende").get("sitzung-ende-uhrzeit")
    sitzung_naechste_datum = ""
    herstellung = ""
    start_seitennr = ""

    el_dbtplenarprotokoll = ET.Element("dbtplenarprotokoll", {
        "wahlperiode": wahlperiode,
        "sitzung-nr": sitzung_nr,
        "sitzung-datum": sitzung_datum,
        "sitzung-start-uhrzeit": sitzung_start_uhrzeit,
        "sitzung-ende-uhrzeit": sitzung_ende_uhrzeit,
        "sitzung-naechste-datum": sitzung_naechste_datum,
        "herstellung": herstellung,
        "start-seitennr": start_seitennr
    })
    el_dbtplenarprotokoll.append(root_toc)
    el_dbtplenarprotokoll.append(root_content)

    with open("2_output/" + file_id + ".xml", "wb") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" ?>\n<!DOCTYPE dbtplenarprotokoll SYSTEM "dbtplenarprotokoll.dtd">\n'.encode('utf8'))
        tree = ET.ElementTree(el_dbtplenarprotokoll)
        ET.indent(el_dbtplenarprotokoll, space="\t", level=0)
        tree.write(f, encoding="utf-8", xml_declaration=False)


def main():
    files_list_content = os.listdir("1_input/content_xml")
    files_list_content.remove(".gitignore")
    files_list_toc = os.listdir("1_input/toc_xml")
    files_list_toc.remove(".gitignore")

    ids_content = [x.split("-")[0] for x in files_list_content]
    ids_toc = [x.split("-")[0] for x in files_list_toc]
    assert ids_content == ids_toc, "IDs in content and toc directories are not the same"

    for file_id in ids_content:
        merge_xml(file_id)


if __name__ == '__main__':
    main()
