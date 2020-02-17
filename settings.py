
class Settings:
    show_timestamps= True
    relative_timestamps= True
    autorange= False
    domain = [-40, 0] # technically its the domain (x axis of the plots
    dashboard_hz= 1
    arduino_hz= 5
    disable_table_column_titles= True
    show_plot_footer= True
    data_missing_value= -999 # use this value to show that there is no data for a variable
    max_len = int((domain[1]-domain[0])*arduino_hz)
    display_mode_bar = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)

        return cls.instance
