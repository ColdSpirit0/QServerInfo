class ServerText():
    @staticmethod
    def decode_text(text):
        return text.encode("raw_unicode_escape").decode("utf-8")

    @staticmethod
    def decode_raw(text):
        return text.encode("raw_unicode_escape")

    @staticmethod
    def decode_recursive(data, tabs=0):
        tabbing = "\t" * tabs
        t = type(data)

        if t is str:
            return f"'{ServerText.decode_text(data)}'"

        elif t is dict:
            s = [""]  # extra line

            for k, v in data.items():
                s.append(
                    tabbing
                    + f"{ServerText.decode_recursive(k)}: [{type(v).__name__}] = {ServerText.decode_recursive(v)}"
                )

            return "\n".join(s)

        elif t is list:
            s = [""]

            for v in data:
                s.append(tabbing + ServerText.decode_recursive(v, tabs + 1))

            return "\n".join(s)

        else:
            return data
