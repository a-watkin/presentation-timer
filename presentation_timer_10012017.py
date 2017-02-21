#!/usr/bin/python3
# presentation_timer_10012017.py by Adam Watkin 
# 2017

try:
    # Python2
    import Tkinter as tk
    from Tkinter import *
    # causing problems with py2exe
    # # changed this from:
    # Tkinter import ttk
    # to this
    import ttk
except ImportError:
    # Python3
    import tkinter as tk
    from tkinter import ttk
    from tkinter import *
import time
# import re
import winsound


class PresentationTimer(Frame):
    def __init__(self, parent, **kw):
        Frame.__init__(self, parent, kw)

        self.counter_val = 0
        # start time
        self.parent = parent
        self.original_remaining_time = 0
        self._start = 0
        # time since the start
        self._remaining_time = 0
        # state
        self._running = 0
        self.timestr = StringVar()
        self.time_to_begin = 0
        # used to make display a blank string
        self.no_text = StringVar()

        # needed
        self.entry = tk.Entry(bd=1)

        # text warnings
        self.first_warning = None
        self.warning_str = StringVar()
        self.blank_str = StringVar()
        self.final_warning = None
        self.final_warning_called = False
        self.first_warning_called = False

        # warning label values
        # somehow these values are growing by the time specified
        # these values are set to originals after running
        # and the originals are set based on entered values for
        # first and final warning
        self.show_warning = 1
        self.show_final_warning = 1

        self.show_warning_original = 0.0
        self.final_warning_original = 0.0

        self.first_countdown = 10
        self.second_countdown = 10

        self.label_warning = None

        # checkbox values
        self.time_delay = 3.0
        self.do_delay = False

        self.delay = IntVar()
        self.first_audio_warning = IntVar()
        self.second_audio_warning = IntVar()

        self.has_run = False

        self.first_warning_over = False
        self.final_warning_over = False

    def _update(self):
        # print('first countdown value is {}'.format(self.first_countdown))
        if self._remaining_time > 0:

            if self.do_delay == True:
                self.time_delay - 1

            self._remaining_time = self._remaining_time - 0.500
            self._setTime(self._remaining_time)

            if self.first_warning_over != True:
                self.check_first_warning()
            if self.final_warning_over != True:
                self.check_final_warning()
            # testing
            self._timer = self.after(500, self._update)

            # added here
            if self._remaining_time == 0:

                # needed to ensure that the entry fields are
                # enabled again when the time is up
                self.text_entry.config(state='enabled')
                self.time_delay_cehckbox.config(state='enabled')
                self.reset_start()
                self.has_run = False

    def check_first_warning(self):
        if (self.first_warning_called is True) and (self.first_countdown > 0):
            # self.show_warning = self.show_warning - 1
            self.first_countdown = self.first_countdown - 1

        if self.valid_first_warning():
            if (self._remaining_time == self.first_warning):
                self.first_warning_called = True

                time_val = self.first_warning
                minutes = int(time_val / 60)
                seconds = int(time_val - minutes * 60.0)
                hseconds = int((time_val - minutes * 60.0 - seconds) * 100)

                if minutes == 1:
                    self.warning_str.set(
                        '{} minute remaining.'.format(minutes))
                else:
                    self.warning_str.set(
                        '{} minutes remaining.'.format(minutes))

                if self.first_audio_warning.get() == 1:
                    self.do_beep()

        if self.first_countdown == 0 and self.first_warning_over == False:
            self.first_warning_over = True
            self.warning_str.set('')

    def check_final_warning(self):
        # it does actually enter here
        # print('final warning called {}, second countdown {}, remaining time {} final warning time {} values equal? {}, final warning over {}'.format(
        #     self.final_warning_called, self.second_countdown,
        #     self._remaining_time, self.final_warning, self._remaining_time == self.final_warning,
        #     self.final_warning_over))

        if (self.final_warning_called is True) and (self.second_countdown > 0):
            self.second_countdown = self.second_countdown - 1

        if self.valid_final_warning():
            if (self._remaining_time == self.final_warning):
                self.final_warning_called = True

                time_val = self.final_warning
                minutes = int(time_val / 60)
                seconds = int(time_val - minutes * 60.0)
                hseconds = int((time_val - minutes * 60.0 - seconds) * 100)
                if minutes == 1:
                    self.warning_str.set(
                        '{} minute remaining.'.format(minutes))
                else:
                    self.warning_str.set(
                        '{} minutes remaining.'.format(minutes))

                if self.second_audio_warning.get() == 1:
                    self.do_beep()

        if self.second_countdown == 0 and self.final_warning_over == False:
            self.final_warning_over = True
            self.warning_str.set('')

    def do_beep(self):
        # winsound.PlaySound(
        #     "whisky_ding_long.wav", winsound.SND_FILENAME)
            
        # the playing of the sound file causes a noticeable delay
        # between the sound and the visual warning
        winsound.PlaySound(
            "whisky_ding_short2.wav", winsound.SND_FILENAME)

    def _setTime(self, _remaining_time):
        # def _setTime(self, _remaining_time):
        if self._remaining_time <= 0:
            self.timestr.set("Time's up.")
            self._running = 0
            assert (self._running == 0)

        elif self._remaining_time > 0:
            minutes = int(_remaining_time / 60)
            seconds = int(_remaining_time - minutes * 60.0)
            # hseconds = int((_remaining_time - minutes * 60.0 - seconds) * 100)
            self.timestr.set('%02d:%02d' % (minutes, seconds))

    def show_first_warning(self):
        self.label_warning = Label(textvariable=self.warning_str)
        self.label_warning.config(font=('Calibri', 22, 'bold'))
        self.label_warning.grid(row=2, column=1, columnspan=4)

    def start(self):
        self.warning_str.set('')

        # does this if it has already run
        if self.has_run == True and not self._running and self.valid_input():
            self.reset_warnings()

            # disabled the presentation time box when running
            self.text_entry.config(state='disabled')

            self.time_delay_cehckbox.config(state='disabled')

            self.start_button = ttk.Button(text='Pause', command=self.stop).grid(
                row=6, column=1, stick='nsew', columnspan=1, rowspan=1, padx=20, pady=20)

            # self.get_presentation_time()
            self.get_firstwarning_time()
            self.get_finalwarning_time()

            # problem
            # so this sort of works, it stops it growing to a point
            # although repeatedly pressing start/pause will all you to
            # get to something like +5 seconds
            delay_temp = self.original_remaining_time + 3
            # print('delay temp is', delay_temp)
            # print('original remaining time is', self.original_remaining_time)
            if self.do_delay is True and (self._remaining_time < delay_temp):
                self._remaining_time = self._remaining_time + self.time_delay

            self._start = time.time() - self._remaining_time
            self._update()
            self._running = 1

        # starts with this
        # _running should be False for this to start
        elif not self._running and self.text_entry.get() != '' and self.valid_input():
            # disabled the presentation time box when running
            self.text_entry.config(state='disabled')

            self.time_delay_cehckbox.config(state='disabled')

            self.has_run = True

            self.start_button = ttk.Button(text='Pause', command=self.stop).grid(
                row=6, column=1, stick='nsew', columnspan=1, rowspan=1, padx=20, pady=20)

            # handle the warnings
            self.reset_warnings()
            self.get_firstwarning_time()
            self.get_finalwarning_time()
            self.get_presentation_time()

            if self.do_delay == True:
                self._remaining_time = self._remaining_time + self.time_delay

            self._start = time.time() - self._remaining_time
            self._update()
            self._running = 1

    def stop(self):
        if self._running:
            self.after_cancel(self._timer)
            self._start = time.time() - self._remaining_time
            self._setTime(self._remaining_time)
            self._running = 0
            # re-enable user input of presentation time
            self.text_entry.config(state='enabled')
            self.time_delay_cehckbox.config(state='enabled')

            self.reset_start()

    def reset_warnings(self):
        # reset how long warning messages are shown
        self.first_countdown = 60
        self.second_countdown = 60

        # reset if warnings have been called
        self.first_warning_called = False
        self.final_warning_called = False

        # reset if warnings are over
        self.first_warning_over = False
        self.final_warning_over = False

    def reset_start(self):
        self.start_button = ttk.Button(text='Start', command=self.start).grid(
            row=6, column=1, stick='nsew', columnspan=1, rowspan=1, padx=20, pady=20)

    def reset(self):
        if self.has_run == True:
            self.reset_warnings()
            self.warning_str.set('')

            self.get_firstwarning_time()
            self.get_finalwarning_time()

            self._start = time.time() - self._remaining_time
            self._remaining_time = self.original_remaining_time
            self.update()

            # something here to make sure the time is correct?
            # this is here because on occasion it does not update
            # properly, but not often so it's difficult to test
            if self._remaining_time != self.original_remaining_time:
                self.update()

            # updates the set time
            self._setTime(self.original_remaining_time)

            # reset presentation time info
            if self.text_entry.get() == '':
                # make sure the input time is in minutes
                # instead of seconds
                self.text_entry.insert(0, int(self.original_remaining_time / 60) )

            self.update()
            self.stop()

    def get_presentation_time(self):
        if self.valid_input():
            temp_time = float(self.text_entry.get())
            temp_time = temp_time * 60
            self._remaining_time = temp_time

    def get_firstwarning_time(self):
        if self.valid_first_warning():
            temp_time = float(self.first_warning_entry.get())
            temp_time = temp_time * 60
            self.first_warning = temp_time

    def get_finalwarning_time(self):
        if self.valid_final_warning():
            temp_time = float(self.final_warning_entry.get())
            temp_time = temp_time * 60
            self.final_warning = temp_time

    def on_entry_click(self, event):
        if self.text_entry.get() == 'in minutes':
            self.text_entry.delete(0, "end")

    def on_warning_click(self, event):
        if self.first_warning_entry.get() == 'before end':
            self.first_warning_entry.delete(0, "end")
            self.final_warning_entry.delete(0, "end")

    def valid_input(self):
        test_if_number = self.text_entry.get()
        if test_if_number.isdigit():
            return True
        else:
            return False

    def valid_first_warning(self):
        test_if_number = self.first_warning_entry.get()
        if test_if_number == '':
            # self.first_warning = 0
            return False
        elif test_if_number.isdigit():
            return True
        else:
            return False

    def valid_final_warning(self):
        test_if_number = self.final_warning_entry.get()
        if test_if_number == '':
            # self.final_warning = 0
            return False
        elif test_if_number.isdigit():
            return True
        else:
            return False

    # problem here
    # if you click on the entry box while it's running
    # it resets the counter
    def on_focusout(self, event):
        if self.valid_input():
            blah = self.text_entry.get()
            blah = int(blah)  # * 60
            blah = blah * 60
            self._remaining_time = blah
            self.original_remaining_time = blah

    def on_outfocus_warnings(self, event):
        self.get_firstwarning_time()
        self.get_finalwarning_time()

    def checkbox_callback(self):
        if self.delay.get() == 1:
            self.do_delay = True
        else:
            self.do_delay = False

    def show_start(self):
        # initial message
        self.timestr.set("Please enter a time below")

        # labels
        self.label = ttk.Label(
            self.master, textvariable=self.timestr, background="", foreground="black")
        self.label.config(justify=CENTER)
        self.label.config(font=('Calibri', 22, 'bold'))

        self.label.grid(row=0, column=1, columnspan=4)
        self.label.grid(row=0, column=1, padx=20, pady=20)

        self.label_warning = Label(textvariable=self.warning_str)
        self.warning_str.set('Warnings will be displayed here')
        self.label_warning.config(font=('Calibri', 22, 'bold'), justify=CENTER)
        self.label_warning.grid(padx=0, pady=10)
        self.label_warning.grid(row=2, column=1, columnspan=4)

        # text entry box labels
        # presentation time
        # self.presentation_time_label = ttk.Label(
        #     text="Presentation time \nin minutes:")

        self.presentation_time_label = ttk.Label(
            text="Presentation time:")
        self.presentation_time_label.grid(row=3, column=1, padx=20, sticky='W')

        # first warning
        self.first_warning_label = ttk.Label(text="First warning \nin minutes:")
        self.first_warning_label.grid(row=4, column=1, padx=20, sticky='W')

        # second warning
        self.second_warning_lable = ttk.Label(text="Final warning \nin minutes:")
        self.second_warning_lable.grid(row=5, column=1, padx=20, sticky='W')

        # text entry boxes
        self.text_entry = ttk.Entry(text="Final minutes remaining warning.")
        self.text_entry.insert(0, 'in minutes')
        self.text_entry.bind('<FocusIn>', self.on_entry_click)
        self.text_entry.grid(
            row=3, column=2, stick='nsew', columnspan=1)
        self.text_entry.insert(0, '')
        self.text_entry.bind('<FocusOut>', self.on_focusout)

        self.first_warning_entry = ttk.Entry(text="text", width=10)
        self.first_warning_entry.insert(0, 'before end')
        self.first_warning_entry.bind('<FocusIn>', self.on_warning_click)
        self.first_warning_entry.grid(
            row=4, column=2, stick='nsew', columnspan=1)
        # added this to get the first warning on the fly
        self.first_warning_entry.bind('<FocusOut>', self.on_outfocus_warnings)

        self.final_warning_entry = ttk.Entry(text="text 2", width=10)
        self.final_warning_entry.insert(0, 'before end')
        self.final_warning_entry.bind('<FocusIn>', self.on_warning_click)
        self.final_warning_entry.grid(
            row=5, column=2, stick='nsew', columnspan=1)
        # added this to get the first warning on the fly
        self.final_warning_entry.bind('<FocusOut>', self.on_outfocus_warnings)

        # checkboxes
        self.time_delay_cehckbox = ttk.Checkbutton(
            text="Delay start by \n3 seconds", variable=self.delay, command=self.checkbox_callback)
        self.time_delay_cehckbox.grid(row=3, column=3, padx=20, columnspan=1)

        self.first_warning_alarm = ttk.Checkbutton(
            text="Audio warning", variable=self.first_audio_warning, command=self.checkbox_callback)
        self.first_warning_alarm.grid(
            row=4, column=3, columnspan=1, padx=20, pady=5, sticky='W')

        self.final_warning_alarm = ttk.Checkbutton(
            text="Audio warning", variable=self.second_audio_warning, command=self.checkbox_callback)
        self.final_warning_alarm.grid(
            row=5, column=3, columnspan=1, padx=20, pady=5, sticky='W')

        # buttons
        self.start_button = ttk.Button(text='Start', command=self.start).grid(
            row=6, column=1, stick='nsew', columnspan=1, rowspan=1, padx=20, pady=20)
        self.reset_button = ttk.Button(text='Reset', command=self.reset).grid(
            row=6, column=2, stick='nsew', columnspan=1, padx=20, pady=20)
        self.quit_button = ttk.Button(text='Quit', command=self.quit).grid(
            row=6, column=3, stick='nsew', columnspan=1, padx=20, pady=20)


def main():
    root = Tk()
    sw = PresentationTimer(root)
    sw.show_start()
    root.title('Presentation Timer')
    root.resizable(False, False)

    # change the tk icon
    root.iconbitmap('pt_icon.ico')
    root.mainloop()


if __name__ == '__main__':
    main()
