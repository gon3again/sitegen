from textnode import TextNode
from textnode import TextType
def main():
    print("hello world")

    my_text_node = TextNode("this is my text", TextType.CODE.value, "google.com")
    print(my_text_node)



if __name__ == "__main__":
    main()
