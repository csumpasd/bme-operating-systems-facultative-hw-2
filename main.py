# second chance memory page management algorithm with a maximum page freeze of 3

MAX_FREEZE_TIME = 3


class Frame:
    def __init__(self, name, page):
        self.name = name
        self.page = page
        self.frozen = 0
        self.referenced = 0
        self.dirty = False


frames = [Frame('A', 0), Frame('B', 0), Frame('C', 0)]
output = ""


def decrease_freeze_times():
    for f in frames:
        if f.frozen > 0:
            f.frozen -= 1


# every comma separated number in input is a page reference
for ref in input().split(','):

    # cast to int, so I don't have to everywhere else
    ref = int(ref)

    # looking for the referenced page in our frames, and if found, we don't have to insert it again
    already_loaded = False
    for frame in frames:
        if frame.page == abs(ref):

            # if it's a read operation then add a reference and remove the freeze
            if ref > 0:
                frame.referenced += 1
                frame.frozen = 0

            # if it's a write operation then just set the frame to dirty (irrelevant with SC but
            else:
                frame.dirty = True

            # either way, we found it, we can decrease freeze times, and happily move on
            decrease_freeze_times()
            already_loaded = True
            output += '-'
            break

    # if we didn't find the page, we have to insert it into the oldest non-frozen non-referenced page's spot
    if not already_loaded:

        i = 0
        while i < len(frames):

            # if the frame is frozen, go on to the next
            if frames[i].frozen > 0:
                i += 1
                continue

            # otherwise, if we can, then decrease freeze times, insert the page, and move the frame to the back
            if frames[i].referenced == 0:

                decrease_freeze_times()

                frames[i].page = abs(ref)
                frames[i].frozen = MAX_FREEZE_TIME
                frames[i].dirty = False if ref > 0 else True

                output += frames[i].name

                frames.append(frames.pop(i))
                break

            # otherwise just remove all references, move the frame to the back, and try again at the same spot
            else:
                frames[i].referenced = 0
                frames.append(frames.pop(i))

        # if we reached the end of the fifo then we couldn't insert the page, and we mark that in the output with a '*'
        if i == len(frames):
            decrease_freeze_times()
            output += '*'


print(output)
print(len(output) - output.count('-'))
