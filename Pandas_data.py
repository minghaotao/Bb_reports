import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
from os import sep
import os


def full_path(filename):
    return f'{sys.path[0]}{sep}{filename}'


current_month = datetime.date.today().strftime('%Y/%m')

filt_month = '2020/08'

partial_month = filt_month.split('/')[1]

partial_year = filt_month.split('/')[0]

headers = ["ID", "Agent", "CallDateTime", "CallDate", "CallTime", "CallDay", "CallCategory", "UserType", "Faculty",
           "Comment", "Department", "ContactType", "BbCategory"]
df = pd.read_csv("CallData8.txt.csv", encoding='ISO-8859-1', names=headers)


def reset_index():
    df['CallDate'] = pd.to_datetime(df['CallDate'], format='%Y/%m/%d')

    df.set_index('CallDate', inplace=True)

    plt.style.use("fivethirtyeight")


def monthy_call():
    monthly_calls = df[filt_month]['UserType'].value_counts()

    def func(pct, allvals):
        absoulte = int(round(pct / 100. * np.sum(allvals)))
        return "{:1.1f}%\n({:d})".format(pct, absoulte)

    if monthly_calls.count() == 3:

        explode = (0, 0.1, 0)
    else:

        explode = (0, 0.1)

    monthly_calls.plot.pie(label='UserType', explode=explode, autopct=lambda pct: func(pct, monthly_calls.tolist()),
                           shadow=True,
                           startangle=90,
                           title="Faculty Vs Student Calls")

    plt.axis('equal')

    plt.savefig('{}/images/1-monthy_call.png'.format(os.getcwd()))

    plt.show()


def contact_type():
    fig, ax = plt.subplots()

    def autolabel(rects, xpos='center'):
        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() * offset[xpos], 1.01 * height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')

    contact_types = df[filt_month]['ContactType'].value_counts()

    # bar_plot = contact_types.plot.bar(figsize=(7, 6), rot=0, title="Contact Methods")

    bar_plot = plt.bar(contact_types.index, contact_types.tolist())

    autolabel(bar_plot)

    plt.title("Contact Methods")

    plt.tight_layout()

    plt.savefig('{}/images/2-contact_type.png'.format(os.getcwd()))

    plt.show()


def Call_categories():
    call_categories = df[filt_month]['CallCategory'].value_counts()

    ax = call_categories.sort_values().plot.barh(fontsize=9, figsize=(7, 6))

    for patch in ax.patches:
        ax.text(
            patch.get_width(),
            patch.get_y(),
            " {:,}".format(patch.get_width()),
            fontsize=10,
            color='dimgrey'
        )

    plt.title("Call Categories")

    plt.tight_layout()

    plt.savefig('{}/images/3-call_categories.png'.format(os.getcwd()))

    plt.show()


def Bb_categroies():
    bb_categories = df[filt_month]['BbCategory'].value_counts()

    ax = bb_categories.plot.bar(fontsize=10, rot=0, figsize=(7, 6))

    for patch in ax.patches:
        ax.text(
            patch.get_x() + .2,
            patch.get_height() + .5,
            " {:,}".format(patch.get_height()),
            fontsize=10,
            color='dimgrey'
        )

    plt.title("Bb Categories")

    plt.tight_layout()

    plt.savefig('{}/images/4-Bb_categories.png'.format(os.getcwd()))

    plt.show()


def Bb_categroies_userType():
    bb_categories_userType = df[filt_month].groupby(['BbCategory']).agg({'UserType': 'value_counts'})[
        'UserType'].unstack().reindex(columns=['Faculty', 'Student', 'GTA']).fillna(0)

    ax = bb_categories_userType.plot.bar(fontsize=9, figsize=(7, 6), rot=0)

    for patch in ax.patches:
        ax.text(
            patch.get_x(),
            patch.get_height() + 1,
            " {:,}".format(int(patch.get_height())),
            fontsize=10,
            color='dimgrey'
        )

    plt.title("Faculty Vs Student")

    plt.tight_layout()

    plt.savefig('{}/images/5-Bb_categoreis_userType.png'.format(os.getcwd()))

    plt.show()

    print(bb_categories_userType)


def Bb_deaprtments():
    department = df[filt_month]['Department'].str.upper().value_counts()
    ax = department.sort_values().plot.barh(fontsize=9, figsize=(7, 6))

    for patch in ax.patches:
        ax.text(
            patch.get_width(),
            patch.get_y(),
            " {:,}".format(patch.get_width()),
            fontsize=10,
            color='dimgrey'
        )
    # x = plt.gca().yaxis
    # for item in x.get_ticklabels():
    #     item.set_rotation(45)

    plt.title("Faculty Calls from Departments")

    plt.tight_layout()

    plt.savefig('{}/images/6-Bb_department.png'.format(os.getcwd()))

    plt.show()


def call_week_days():
    call_day = df[filt_month]['CallDay'].sort_values().value_counts()

    ax = call_day.plot.bar(fontsize=9, figsize=(7, 6), rot=0)

    for patch in ax.patches:
        ax.text(
            patch.get_x() + .1,
            patch.get_height() + .5,
            " {:,}".format(patch.get_height()),
            fontsize=10,
            color='dimgrey'
        )

    plt.title("Call Week Days")

    plt.tight_layout()

    plt.savefig('{}/images/7-call_week_days.png'.format(os.getcwd()))

    plt.show()


def call_hours():
    # call_hours = df[filt_month]['CallTime'].hour().resample('H').agg({'value_counts'})

    # call_hours = df[filt_month]['CallDateTime'].values.strftime('%H')
    # call_hours = df[filt_month].groupby(['CallDateTime']).agg({'UserType': 'value_counts'})

    call_hours = df[filt_month]['CallTime']
    call_hours = pd.DatetimeIndex(call_hours.values).strftime('%H').value_counts().sort_index()

    call_hours.plot.area(fontsize=9, figsize=(8, 6), rot=0)

    plt.title("Call Hours")

    plt.xlabel('8:00 AM - 6:00 PM')

    # plt.subplots_adjust(bottom=0.2)

    plt.tight_layout()

    plt.savefig('{}/images/8-call_hours.png'.format(os.getcwd()))

    plt.show()

    print(call_hours)
    # print(type(call_hours))
    # print(call_hours.index)
    # print(call_hours_count)


def call_days():
    call_days = df[filt_month]['UserType'].resample('D').agg({'value_counts'})[
        'value_counts'].unstack().reindex(columns=['Faculty', 'Student', 'GTA']).fillna(0)

    call_days.index = call_days.index.strftime('%m-%d(%a)')

    call_days.plot.area(fontsize=9, figsize=(9, 7), rot=0, stacked=False)

    plt.title('Call trends')

    plt.xlabel('Year of {}'.format(partial_year))

    plt.tight_layout()

    plt.savefig('{}/images/9-call_days.png'.format(os.getcwd()))

    plt.show()

    print(call_days)


def monthly_comparison():
    monthly_calls = df['UserType'].resample('M').agg({'value_counts'})[
        'value_counts'].unstack().reindex(columns=['Faculty', 'Student', 'GTA']).fillna(0)

    monthly_calls = monthly_calls[monthly_calls.index.month == int(f"{partial_month}")].sort_index(ascending=False)

    print(monthly_calls)
    print(type(monthly_calls))

    monthly_calls.index = monthly_calls.index.strftime('%Y-%b')

    ax = monthly_calls.plot.bar(fontsize=9, figsize=(7, 6), rot=0)

    for patch in ax.patches:
        ax.text(
            patch.get_x(),
            patch.get_height() + 2,
            " {:,}".format(int(patch.get_height())),
            fontsize=10,
            color='dimgrey'
        )

    plt.xlabel('Current Year of {}'.format(partial_year))

    plt.title("Monthly calls Comparison")

    plt.tight_layout()

    plt.savefig('{}/images/90-monthly_camparison.png'.format(os.getcwd()))

    plt.show()

    # print(monthly_calls)


def call_years():
    # monthly_calls = df[current_year]['UserType'].groupby([df['CallDate'].dt.month.rename('month')]).agg(
    #     {'value_counts'})

    monthly_calls = df[partial_year]['UserType'].sort_values().resample('M').agg({'value_counts'})[
        'value_counts'].unstack().reindex(columns=['Faculty', 'Student', 'GTA']).fillna(0)

    monthly_calls.index = monthly_calls.index.strftime('%Y-%b')

    ax = monthly_calls.plot.bar(fontsize=9, figsize=(7, 6), rot=0)

    for patch in ax.patches:
        ax.text(
            patch.get_x(),
            patch.get_height() + 2,
            " {:,}".format(int(patch.get_height())),
            fontsize=10,
            color='dimgrey'
        )
    # Adjust the xaxis postion to re-rotate
    # x = plt.gca().xaxis
    # for item in x.get_ticklabels():
    #     item.set_rotation(45)
    # plt.subplots_adjust(bottom=0.25)

    plt.xlabel('Year of {}'.format(partial_year))

    plt.title("Monthly calls - Faculty/Student")

    plt.tight_layout()

    plt.savefig('{}/images/91-call_years.png'.format(os.getcwd()))

    plt.show()

    # print(monthly_calls.index.tolist())
    # print(monthly_calls['value_counts'])
    # print(set_index)
    # print(monthly_calls.values)

    # print(monthly_calls.index.get_level_values(1))
    # print(monthly_calls.values.tolist())
    # print(monthly_calls.index)
    #
    # print(monthly_calls.index[0])
    #
    # print(type(monthly_calls.index))
    #
    # print(monthly_calls)


def requestCat():


    rows = {'CourseCopy':[319],'CourseMerge':[138]}
    df = pd.DataFrame(data=rows)

    print(df)
    ax = df.plot.bar(fontsize=9, figsize=(7, 6), rot=0)

    for patch in ax.patches:
        ax.text(
            patch.get_x(),
            patch.get_height() + 2,
            " {:,}".format(int(patch.get_height())),
            fontsize=10,
            color='dimgrey'
        )

    plt.tight_layout()
    plt.title("RequestCat Fall 2020")
    plt.show()


def main():
    # print(monthy_call())
    # print(contact_type())
    # print(Bb_categroies())
    # print(Call_categories())
    print(Bb_deaprtments())
    # print(Bb_categroies_userType())
    # print(call_hours())
    # print(call_week_days())
    # print(call_days())
    # print(monthly_comparison())
    # print(call_years())
    print(requestCat())


if __name__ == '__main__':
    reset_index()
    main()
