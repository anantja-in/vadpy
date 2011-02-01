import os

# modules PATH
PATH = ['./modules',
        ]

ROOT = os.path.abspath('..')

format_args = {
    'root' : ROOT, 
    'bindir' : ROOT + '/bin',
    'outdir' : ROOT + '/output',
    'dbdir' :  ROOT + '/databases',
    'framelen' : 0.01,            
}

MACROS = {   
    # macros 
    'mcr_io'         : 'path-attr="" frame-len={framelen}',
    'mcr_basevad'    : 'voutdir="{{outdir}}/{{modname}}" outpath="{{voutdir}}/{{srcname}}/{{srcfile}}" overwrite=No',
    'mcr_labels_vad' : 'labels-attr="vad_labels" path-attr="vout_path"',
    'mcr_labels_gt'  : 'labels-attr=gt_labels path-attr=gt_path',
    'mcr_compare'    : 'sep-sources=Yes inputs=gt_labels,vad_labels',

    # Default modules' configurations
    'dft_dbnist05'  : 'dbnist05 dataset=""',
    'dft_dbnist08'  : 'dbnist08 dataset="" dataunits="" channels=""',
    'dft_iosingled' : 'iosingled mcr_io k=1',
    'dft_iostamps'  : 'iostamps mcr_io',
    'dft_iogapless' : 'iogapless mcr_io',
    'dft_matlab'    : 'vadmatlab mcr_basevad voutdir="{outdir}/matlab/{{engine}}_{{script}}" bin=matlab mopts="-nojvm, -nosplash" ' \
                      'scriptdir={bindir}/matlab fread=600 filecount=128 args=""',
    'dft_info'       : 'modinfo action=show',
    'dft_cat'        : 'modcat gt=yes source=yes',
    'dft_edit'       : 'modedit attr="" value={{attr}}',
    'dft_confusion'  : 'modconfusion mcr_compare',

    # DB modules
    'nist05' : 'dft_dbnist05 root="{dbdir}/NIST05" source-dir=DATA gt-dir=GT/ASR',
    'nist08' : 'dft_dbnist08 root="{dbdir}/NIST08" source-dir=DATA gt-dir=GT',    

    #IO modules
    'inist'     : 'dft_iostamps re=(?P<ss>\d.+) split=" " action=read labels-attr=gt_labels path-attr=gt_path ',
    'isingle'   : 'dft_iosingled mcr_labels_gt action=read ', 
    'ivsingle'  : 'dft_iosingled mcr_labels_vad action=read', 
    'igapless'  : 'dft_iogapless action=read',
    'ogapless'  : 'dft_iogapless mcr_labels_gt action=write',
    'ovstamps'  : 'dft_iostamps mcr_labels_vad re="" split="" action=write', 
    'ovsingle'  : 'dft_iosingled mcr_labels_vad action=write',
    'ovgapless' : 'dft_iogapless mcr_labels_vad action=write',
    # VAD->IO shortcuts
    'iamr'      : 'ivsingle',
    
    # VAD modulse
    'g729'     : 'vadg729 mcr_basevad voutdir="{outdir}/g729" exec-path="{bindir}/g729/g729vad" ',
    'amr1'     : 'vadamr mcr_basevad voutdir="{outdir}/amr1" exec-path="{bindir}/amr/amr1" ',
    'amr2'     : 'vadamr mcr_basevad voutdir="{outdir}/amr2" exec-path="{bindir}/amr/amr2" ',
    'matlab'   : 'dft_matlab engine=vad',
    'svmtrain' : 'dft_matlab engine=svm script=train',
    'svmtest'  : 'dft_matlab engine=svm script=test',

    # Other modules
    'cat'  : 'dft_cat',
    'info' : 'dft_info',
    'edit'      : 'dft_edit', 
    'confusion' : 'dft_confusion',
}
