import xml.etree.ElementTree as etree

template_file = "intro_concat.tpl.mlt"
output_file = "intro_concat.mlt"
input_files = [
    "01.mlt",
    "02_prestaveni_helmy.mlt",
    "03.mlt",
    "04_zbrojeni_knezek.mlt",
    "05.mlt",
    "06_firefly_bojuje.mlt",
    "07.mlt"
]

def get_playlist0(tree):
    return [ x for x in tree.getroot().findall("playlist") if x.attrib["id"] == "playlist0" ][0]

template_tree = etree.parse(template_file)
tgt_playlist = get_playlist0(template_tree)

producer_counter = 0
for infile in input_files:
    tree = etree.parse(infile)
    playlist0 = get_playlist0(tree)

    # list playlist items and corresponding producers
    timeline_elements = [ (x, [y
                                for y in tree.getroot().findall("producer") if y.attrib["id"] == x.attrib["producer"]
                                ][0])
                           for x in playlist0.findall("entry") if x.attrib["producer"].startswith("producer") ]

    for timeline_entry, producer in timeline_elements:
        producer_name = "producer" + str(producer_counter)
        # rename and add producer
        producer.attrib["id"] = producer_name
        template_tree.getroot().insert(1, producer)
        # rename and add playlist item
        timeline_entry.attrib["producer"] = producer_name
        tgt_playlist.append(timeline_entry)

        producer_counter += 1

# dump to ouptut file
template_tree.write(output_file)
