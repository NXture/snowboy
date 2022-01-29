
import argparse
import tempfile
import uuid
from scipy.io import wavfile
from pmdl import snowboy_pmdl_config
from pmdl.snowboy_pmdl import SnowboyPersonalEnroll, SnowboyTemplateCut

def check_enroll_output(enroll_ans):
    if enroll_ans == -1:
        raise Exception("Error initializing streams or reading audio data")
    elif enroll_ans == 1:
        raise Exception("Hotword is too long")
    elif enroll_ans == 2:
        raise Exception("Hotword is too short")


def main():
    parser = argparse.ArgumentParser(description='Command line client for generating snowboy personal model')
    parser.add_argument('-r1', '--record1', dest="record1", required=True, help="Record voice 1")
    parser.add_argument('-r2', '--record2', dest="record2", required=True, help="Record voice 2")
    parser.add_argument('-r3', '--record3', dest="record3", required=True, help="Record voice 3")
    parser.add_argument('-r4', '--record4', dest="record4", required=True, help="Record voice 4")
    parser.add_argument('-r5', '--record5', dest="record5", required=True, help="Record voice 5")
    parser.add_argument('-r6', '--record6', dest="record6", required=True, help="Record voice 6")
    parser.add_argument('-r7', '--record7', dest="record7", required=True, help="Record voice 7")
    parser.add_argument('-r8', '--record8', dest="record8", required=True, help="Record voice 8")
    parser.add_argument('-r9', '--record9', dest="record9", required=True, help="Record voice 9")
    parser.add_argument('-r10', '--record10', dest="record10", required=True, help="Record voice 10")
    parser.add_argument('-n', '--name', dest="model_name", required=True, help="Personal model name")
    parser.add_argument('-lang', '--language', default="en", dest="language", help="Language")
    args = parser.parse_args()

    print("template cut")
    cut = SnowboyTemplateCut(
        resource_filename=snowboy_pmdl_config.get_enroll_resource(args.language))

    out = tempfile.NamedTemporaryFile()
    model_path = str(out.name)

    print("personal enroll")
    enroll = SnowboyPersonalEnroll(
        resource_filename=snowboy_pmdl_config.get_enroll_resource(args.language),
        model_filename=model_path)

    assert cut.NumChannels() == enroll.NumChannels()
    assert cut.SampleRate() == enroll.SampleRate()
    assert cut.BitsPerSample() == enroll.BitsPerSample()
    print("channels: %d, sample rate: %d, bits: %d" % (cut.NumChannels(), cut.SampleRate(), cut.BitsPerSample()))

    recording_set = [args.record1, args.record2, args.record3, args.record4, args.record5, args.record6, args.record7, args.record8, args.record9, args.record10]
    for rec in recording_set:
        print("processing %s" % rec)
        _, data = wavfile.read(rec)
        data_cut = cut.CutTemplate(data.tobytes())
        enroll_ans = enroll.RunEnrollment(data_cut)

    check_enroll_output(enroll_ans)

    filename = args.model_name
    print("saving file to %s" % filename)
    f = open(filename, "wb")
    f.write(open(out.name).read())
    f.close()
    print("finished")

if __name__ == "__main__":
    main()
