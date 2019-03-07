#! python3
# searchnews.py - Searches and displays top results from google news from the last 24h


import requests, webbrowser, bs4, tkinter as tk


# GUI Class
class Gui:

    # initializing window
    def __init__(self):
        self.root = tk.Tk()  # main window
        self.root.title("Latest News by Ricardo Ferreira")
        self.root.geometry("{}x{}".format(600, 700))
        self.root.configure(background="grey")

        # Creating frames
        self.top_frame = tk.Frame(self.root, bg="white")  # logo, searchlabel, text input and search button
        self.bottom_frame = tk.Frame(self.root, bg="grey")  # exit
        self.center_frame = tk.Frame(self.root, bg="grey")  # search results
        self.top_frame.pack(fill=tk.BOTH)
        self.center_frame.pack(side=tk.TOP)
        self.bottom_frame.pack(side=tk.BOTTOM)

        self.searchlabel = tk.Label(self.top_frame, text="Enter the topic you would like to search:", bg="white",
                                    fg="black",
                                    font="none 12 bold")
        self.searchlabel.pack(side=tk.TOP)

        self.textentry = tk.Entry(self.top_frame, width=50, bg="white")
        self.textentry.pack(side=tk.TOP)

        self.searchbutton = tk.Button(self.top_frame, text="SEARCH", width=10, command=self.click)
        self.searchbutton.pack(side=tk.TOP)

        # Bottom frame initialization
        self.exitbutton = tk.Button(self.bottom_frame, text="EXIT", width=10, command=self.close_window)
        self.exitbutton.pack(side=tk.BOTTOM)

        self.root.mainloop()

    # Search button clicking - Gets first page results from google news and returns the title and link from the top 20
    def click(self):

        # Destroying current center_frame with previous results and start a new one
        self.center_frame.destroy()
        self.center_frame = tk.Frame(self.root, bg="grey")
        self.center_frame.pack(side=tk.TOP)

        entered_text = self.textentry.get()  # collecting the text from the text entry box
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"}

        req = requests.get("http://news.google.com/search?q=" + entered_text + "+when:1d", timeout=5, headers=headers)
        soup = bs4.BeautifulSoup(req.text, "html.parser")

        # There is some variation between where google news returns, it can be with "h4" or "h3"
        res = soup.find_all("h4")
        if not res:
            res = soup.find_all("h3")

        if res:
            # Initializing the results dict
            self.results = {}
            i = 0
            for each in res[:min(len(res), 20)]:
                # Association between title and url
                self.results[each.get_text()] = "http://news.google.com" + each.find("a")["href"]

            for k, v in self.results.items():
                # Creating the results buttons, text = news title, action = open the respective url
                tk.Button(self.center_frame, text=k, command=lambda v=v: self.openlink(v)).pack(side=tk.TOP)
                i += 1
        else:
            # When no results are found
            tk.Label(self.center_frame, text="No Results Found").pack(side=tk.TOP)

    # Open url
    def openlink(self, v):
        webbrowser.open(v)

    # Closing window
    def close_window(self):
        self.center_frame.destroy()
        self.top_frame.destroy()
        self.bottom_frame.destroy()
        self.root.destroy()
        exit()


if __name__ == "__main__":
    window = Gui()
    window.root.mainloop()
