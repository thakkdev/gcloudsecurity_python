from util import barchartvalue, readfilefrombucket, createdf
import matplotlib.pyplot as plt


def plotgraph():
    # File 1 metrics 
    file1datestr = 'Jan 4 - Jan 10 2021'
    dfFile1 = createdf(readfilefrombucket('graphbucket_test','Jan 4 - Jan 10 2021.csv'))

    # File 2 metrics 
    file2datestr = 'Jan 11 - Jan 17 2021'
    dfFile2 = createdf(readfilefrombucket('graphbucket_test','Jan 11 - Jan 17 2021.csv'))

    #File 3 metrics 
    file3datestr = 'Jan 18 - Jan 24 2021'
    dfFile3 = createdf(readfilefrombucket('graphbucket_test','Jan 18 - Jan 24 2021.csv'))

    #File 4 metrics 
    file4datestr = 'Jan 25 - Jan 31 2021'
    dfFile4 = createdf(readfilefrombucket('graphbucket_test','Jan 25 - Jan 31 2021.csv'))


    # plotting graph
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.tight_layout()
    fig.suptitle('API transactions over 4 weeks', size=8)

   
    #######File 1 Plot###############
    ax1.set_ylabel('Seconds', size=8)
    ax1.set_title(file1datestr, size=7)
    ax1.set_xticks(dfFile1['id'])
    ax1.tick_params(axis="x", labelsize=6)
    ax1.tick_params(axis="y", labelsize=6)


    ppbar1 = ax1.bar(dfFile1['id'], dfFile1['responsetimeorcount']/1000, color='royalblue', alpha=0.7)
    ax1.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)

    barchartvalue(ppbar1,ax1) # display value on top of each bar
    
    
    #######File 2 Plot###############
    ax2.set_ylabel('Seconds', size=8)
    ax2.set_title(file2datestr, size=7)
    ax2.set_xticks(dfFile2['id'])
    ax2.tick_params(axis="x", labelsize=6)
    ax2.tick_params(axis="y", labelsize=6)

    ppbar2 = ax2.bar(dfFile2['id'], dfFile2['responsetimeorcount']/1000, color='royalblue', alpha=0.7)
    ax2.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    barchartvalue(ppbar2,ax2) # display value on top of each bar


    #######File 3 Plot###############
    ax3.set_ylabel('Seconds', size=8)
    ax3.set_title(file3datestr, size=7)
    ax3.set_xticks(dfFile3['id'])
    ax3.tick_params(axis="x", labelsize=6)
    ax3.tick_params(axis="y", labelsize=6)

    ppbar3 = ax3.bar(dfFile3['id'], dfFile3['responsetimeorcount']/1000, color='royalblue', alpha=0.7)
    ax3.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    barchartvalue(ppbar3,ax3) # display value on top of each bar
    
    #######File 4 Plot###############
    ax4.set_ylabel('Seconds', size=8)
    ax4.set_title(file4datestr, size=7)
    ax4.set_xticks(dfFile4['id'])
    ax4.tick_params(axis="x", labelsize=6)
    ax4.tick_params(axis="y", labelsize=6)

    ppbar4 = ax4.bar(dfFile4['id'], dfFile4['responsetimeorcount']/1000, color='royalblue', alpha=0.7)
    ax4.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    barchartvalue(ppbar4,ax4) # display value on top of each bar
    
    return fig #instead of plt.show() we return fig for creating image
    

