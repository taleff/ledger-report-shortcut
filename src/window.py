import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from report import gen_net_worth_graph, gen_expenses_bar_chart, \
    get_subscriptions, get_top_expenses, get_savings_rate
from theme import SPACING, FONTS, COLORS

class ReportApp(ctk.CTk):
    def __init__(self, filename):
        super().__init__()

        # Configure window
        self.title("Financial Report")
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        # Add cards corresponding to each piece of information of
        # interest
        stats_frame = StatsFrame(self, filename)
        stats_frame.grid(
            column=0, row=0, columnspan=2, sticky='nsew',
            padx=SPACING['frame_padding'],
            pady=(SPACING['frame_padding'], 0)
        )
        
        net_worth_frame = GraphFrame(self, filename, 'net_worth')
        net_worth_frame.grid(
            column=0, row=1, sticky='nsew',
            padx=SPACING['frame_padding'],
            pady=SPACING['frame_padding']
        )

        expenses_bar_frame = GraphFrame(self, filename, 'expenses')
        expenses_bar_frame.grid(
            column=1, row=1, sticky='nsew',
            padx=(0, SPACING['frame_padding']),
            pady=SPACING['frame_padding']
        )

        
class StatsFrame(ctk.CTkFrame):
    def __init__(self, primary, filename):
        super().__init__(primary)

        # Configuring the frame
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        # Savings rate section
        savings_rate = get_savings_rate(filename)
        SAVINGS_THRESHOLD = 20
        if savings_rate >= SAVINGS_THRESHOLD:
            savings_mark, savings_color = '✓', COLORS['success']
        else:
            savings_mark, savings_color = '✗', COLORS['danger']

        savings_header = ctk.CTkLabel(
            self, text='Savings Rate', font=FONTS['title']
        )
        savings_header.grid(
            column=0, row=0, pady=SPACING['header_padding']
        )

        savings_value = ctk.CTkLabel(
            self, text='{}% {}'.format(savings_rate, savings_mark),
            font=FONTS['subtitle'], text_color=savings_color
        )
        savings_value.grid(column=0, row=1, sticky='n')

        # Subscriptions section
        subs_header = ctk.CTkLabel(
            self, text='Subscriptions', font=FONTS['title']
        )
        subs_header.grid(
            column=1, row=0, pady=SPACING['header_padding']
        )
        subs_list = self.scrollable_stat('subscriptions', filename)
        subs_list.grid(
            column=1, row=1, pady=(0, SPACING['header_padding'])
        )

        # Top Payees section
        payee_header = ctk.CTkLabel(
            self, text='Top Payees', font=FONTS['title']
        )
        payee_header.grid(
            column=2, row=0, pady=SPACING['header_padding']
        )
        payee_list = self.scrollable_stat('payees', filename)
        payee_list.grid(
            column=2, row=1, pady=(0, SPACING['header_padding'])
        )

    def scrollable_stat(self, variety, filename):
        list_types = {
            'subscriptions': get_subscriptions,
            'payees': get_top_expenses
        }
        
        left_col, right_col = list_types[variety](filename)

        financial_list = ctk.CTkScrollableFrame(self)
        financial_list.grid_columnconfigure(0, weight=1)
        financial_list.grid_columnconfigure(1, weight=1)
        for i in range(len(left_col)):
            ctk.CTkLabel(financial_list, text=left_col[i]).grid(
                column=0, row=i
            )
            ctk.CTkLabel(financial_list, text=right_col[i]).grid(
                column=1, row=i
            )
            financial_list.grid_rowconfigure(i, weight=1)
            
        return financial_list


class GraphFrame(ctk.CTkFrame):
    def __init__(self, primary, filename, variety):
        super().__init__(primary)

        # Information for the different types of graph cards generated
        # using this class
        header_types = {
            'net_worth': 'Net Worth Over Time',
            'expenses': 'Expense Balances'
        }
        graph_types = {
            'net_worth': gen_net_worth_graph,
            'expenses': gen_expenses_bar_chart
        }

        # Widgets generated in the graph card
        graph_header = ctk.CTkLabel(
            self, text=header_types[variety], font=FONTS['title']
        )
        graph_header.grid(
            column=0, row=0, pady=SPACING['header_padding']
        )

        financial_graph = FigureCanvasTkAgg(
            graph_types[variety](filename), self
        )
        financial_graph.get_tk_widget().grid(
            column=0, row=1
        )
        
