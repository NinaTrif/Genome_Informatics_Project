class Alignment:
    """ Class used for storing alignment details """

    def __init__(self, position, score, transcript, is_reversed, is_valid=True):
        self.position = position
        self.alignment_score = score
        self.edit_transcript = transcript
        self.is_reversed = is_reversed
        self.is_valid = is_valid
