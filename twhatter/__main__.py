from twhatter.client import ClientTimeline
from twhatter.output import Print


user = "the_english_way"
timeline = ClientTimeline(user)

for t in timeline:
    Print(t)()
