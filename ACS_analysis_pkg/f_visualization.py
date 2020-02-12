import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def plot_ratio_ordered(sex_full):
    dict_color ={'SEX': 'C4', 'JOB': 'C3',
            'AGE': 'C2', 'RACE': 'C1',
            'EDU': 'C0'}
    sns.set_style('whitegrid')
    sex_full_sort = sex_full.groupby(['Category']).agg('mean').reset_index()
    sex_full_sort = sex_full_sort.sort_values(by=['F_M_Ratio_Avg'])
    sex_full_list = sex_full_sort['Category'].tolist()
    sns.catplot(y='F_M_Ratio_Avg', x='Category', hue='Variable', data=sex_full,
                dodge=False, kind='bar', palette=dict_color,
                height=4, aspect=3, order=sex_full_list)
    plt.xticks(rotation=60)
    plt.ylim(0,1)
    plt.ylabel('Gendered Wage Ratio (F/M)')
    plt.title('Wage Ratio vs. Categories')


def plot_sex_n_cat(yearly_sex_sep):
    sns.catplot(y='Wage_Avg', x='Sex', hue='Category', col='Variable',
        aspect=0.3, height=6, data=yearly_sex_sep)



def plot_heatmap_lineplot(cat_full, yearly_sex_full, var):
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))

    color_dict = {'SEX': 'coolwarm', 'JOB': 'RdPu',
                    'AGE': 'YlGn', 'RACE': 'Oranges',
                    'EDU': 'Blues'}
    color = color_dict[var]
    heatmap_group = cat_full.loc[(cat_full.Variable == var)]
    if var == 'EDU':
        edu_dict = {
            'No_Highschool': 'N_HS', 
            'Highschool': 'HS',
            'Some_College': 'CLG', 
            'B.S._Degree': 'BS',
            'M.S._Degree': 'MS', 
            'PhD_or_Prof': 'PhD'
            }
        heatmap_group['Category'] = heatmap_group['Category'].map(edu_dict)
        heatmap_group['Base_Category'] = heatmap_group['Base_Category'].map(edu_dict)
    
    elif var == 'JOB':
        job_dict = {
            'Business': 'BUS',
            'Science': 'SCI',
            'Art': 'ART',
            'Healthcare': 'HLC',
            'Services': 'SRV',
            'Sales': 'SAL',
            'Maintenance': 'MTN',
            'Production': 'PRD',
            'Transport': 'TRP',
            'Military': 'MTY'
        }
        heatmap_group['Category'] = heatmap_group['Category'].map(job_dict)
        heatmap_group['Base_Category'] = heatmap_group['Base_Category'].map(job_dict)

    heatmap_group = heatmap_group.groupby(['Category', 'Base_Category']) \
        ['Ratio_vs_Base'].agg(['count','mean','std']).reset_index()
    heatmap_group = heatmap_group.pivot('Category', 'Base_Category', 'mean')
    heatmap_group['sum'] = heatmap_group.iloc[:, :].sum(axis=1)
    heatmap_group = heatmap_group.sort_values(by=['sum'], ascending=False)
    heatmap_group = heatmap_group.drop(columns=['sum'])
    heatmap_group = heatmap_group[list(heatmap_group.index)]
    sns.heatmap(heatmap_group, annot=True, linewidths=.5, cbar=False, 
                cmap = color, fmt='.1f', ax=ax[0])
    ax[0].title.set_text('Heatmap of %s' % var)

    sns.set_style('whitegrid')
    ratio_yearly = yearly_sex_full.loc[(yearly_sex_full.Variable == var)]

    sns.lineplot(x='Year', y='F_M_Ratio_Avg', hue='Category', data=ratio_yearly, ax=ax[1])
    ax[1].set(xlim=(2008, 2018), ylim=(0.70, 0.93))
    ax[1].get_legend().remove()
    ax[1].set_ylabel('Wage Ratio (F/M)')
    ax[1].title.set_text('Wage F / Wage M for each %s group (2008-2018)' % var)

    sns.lineplot(x='Year', y='F_Pct_Ct', hue='Category', data=ratio_yearly, ax=ax[2])
    ax[2].set(xlim=(2008, 2018))
    ax[2].legend(bbox_to_anchor=(1, 1))
    ax[2].set_ylabel('Percent Female')
    ax[2].title.set_text('Percent Female for each %s group (2008-2018)' % var)


def plot_heatmap_basecat(cat_full, var):
    color_dict = {'SEX': 'coolwarm', 'JOB': 'RdPu',
                    'AGE': 'YlGn', 'RACE': 'Oranges',
                    'EDU': 'Blues'}
    color = color_dict[var]
    plt.figure(figsize=(7,7))
    heatmap_group = cat_full.loc[(cat_full.Variable == var)]
    heatmap_group = heatmap_group.groupby(['Category', 'Base_Category']) \
        ['Ratio_vs_Base'].agg(['count','mean','std']).reset_index()
    heatmap_group = heatmap_group.pivot('Category', 'Base_Category', 'mean')
    heatmap_group['sum'] = heatmap_group.iloc[:, :].sum(axis=1)
    heatmap_group = heatmap_group.sort_values(by=['sum'], ascending=False)
    heatmap_group = heatmap_group.drop(columns=['sum'])
    heatmap_group = heatmap_group[list(heatmap_group.index)]
    sns.heatmap(heatmap_group, annot=True, linewidths=.5, cbar=False, 
                cmap = color, fmt='.1f')