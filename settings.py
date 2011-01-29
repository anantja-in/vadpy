# Required constants

# modules PATH
PATH = ['./modules',
        ]

ROOT = '..'                 # {root}

format_args = {
    'root' : ROOT, 
    'bindir' : ROOT + '/bin',
    'outdir' : ROOT + '/output',
    'dbdir' :  ROOT + '/databases',
    'iframelen' : 0.01,            # input frame lengthIFRAMELEN, 
    'oframelen' : 0.01,            # output frame length
}

MACROS = {   
    # Default modules configuration
    'dft_dbnist05' : 'dbnist05 dataset=""',
    'dft_dbnist08' : 'dbnist08 dataset="" dataunits="" channels=""',
    'dft_iosingled' : 'iosingled k=1',
    'dft_vad' : 'voutdir="{{outdir}}/{{modname}}" outpath="{{voutdir}}/{{srcname}}/{{srcfile}}" overwrite=No',
    'dft_info' : 'modinfo action=show',
    'dft_cat' : 'modcat gt=yes source=yes',
    'dft_edit' : 'modedit attr="" value={{attr}}',

    # DB macros
    'nist05' : 'dft_dbnist05 root="{dbdir}/NIST05" source-dir=DATA gt-dir=GT',
    'nist08' : 'dft_dbnist08 root="{dbdir}/NIST08" source-dir=DATA gt-dir=GT',
    
    #IO macros
    'inist' : 'iostamps re=(?P<ss>\d.+) split=" " action=read labels-attr=gt_labels path-attr=gt_path frame-len={iframelen}',
    'isingle' : 'dft_iosingled action=read frame-len={iframelen} k=1 labels-attr=gt_labels path-attr=gt_path', 
    'ivsingle' : 'dft_iosingled action=read frame-len={iframelen} k=1 labels-attr=vad_labels path-attr=vout_path', 
    'ostamps' : 'iostamps re="" split="" action=write frame-len={oframelen} labels-attr=vad_labels path-attr=vout_path', 
    'osingle' : 'iosingled action=write frame-len={oframelen}',

    # VAD macros
    'g729' : 'vadg729 dft_vad voutdir="{outdir}/g729" exec-path="{bindir}/g729/g729vad" ',
    'amr1' : 'vadamr dft_vad voutdir="{outdir}/amr1" exec-path="{bindir}/amr/amr1" ',
    'amr2' : 'vadamr dft_vad voutdir="{outdir}/amr2" exec-path="{bindir}/amr/amr2" ',
    'matlab' : 'vadmatlab dft_vad voutdir="{outdir}/matlab" bin=matlab mopts="-nojvm, -nosplash" ' \
               'scriptdir={bindir}/matlab engine=vad script="" fread=600 filecount=128 args=""',
    'svmtrain' : 'matlab engine=train',
    'svmtest' : 'matlab engine=test',
    'mtest' : 'matlab engine=vad',

    # Other modules' macros
    'dbcat': 'cat outdir="{outdir}"',
    'info' : 'dft_info',
    'edit' : 'dft_edit', 
}
