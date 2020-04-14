import speech_recognition as sr
from processory import Processor


def my_command():
    while True:
        code = yield 'keyboard', "Enter to hear or type for command"
        if code != "":
            yield 'kb_input', code
            continue
        r = sr.Recognizer()
        with sr.Microphone() as source:
            yield 'info', "Hearing..."
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        yield 'info', "Heard something, recognizing"
        try:
            command = r.recognize_google(audio).lower()
            yield 'input', command
        # loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            yield 'exception', "Recognized nothing"


def assistant(command_gen, process):
    mark, msg = next(command_gen)
    while True:
        if mark == 'keyboard':
            print(f"~ {msg}\n> ", end="")
            mark, msg = command_gen.send(input())
        elif mark == 'info':
            print("i", msg)
            mark, msg = next(command_gen)
        elif mark == 'exception':
            print("!", msg)
            mark, msg = next(command_gen)
        elif mark == 'input' or mark == 'kb_input':
            if mark == 'input':
                print(">", msg)
            dowhat, extra = process(msg)
            if dowhat == 'back_err':
                print("!<", extra)
            elif dowhat == 'exit':
                return
            else:
                print("!", "Not implemented!")
            mark, msg = next(command_gen)


processor = Processor()


@processor.register
def exit(*args):
    return 'exit', None


if __name__ == '__main__':
    assistant(my_command(), processor.process)
