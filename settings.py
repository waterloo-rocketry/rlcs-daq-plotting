
class Settings:
    show_timestamps= True
    relative_timestamps= False
    autorange= False
    domain = [-120, 0] # how long back in time to plot
    dashboard_hz = 3
    arduino_hz = 3
    disable_table_column_titles= True
    show_plot_footer= True
    data_missing_value= -999 # use this value to show that there is no data for a variable
    max_len = int((domain[1]-domain[0])*arduino_hz)
    display_mode_bar = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)

        return cls.instance
