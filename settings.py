import os
import getpass

# modules PATH
PATH = ['./modules',
        ]

ROOT = os.path.abspath('..')

format_args = {
    'root' : ROOT, 
    'binroot' : ROOT + '/bin',
    'outroot' : ROOT + '/output/' + getpass.getuser(),
    'dbroot' :  ROOT + '/databases',
}

MACROS = {   
    # configuration values
    'conf_framelen'  : 'frame-len=0.01',

    # macros 
    'mcr_io'         : 'conf_framelen path-attr=""',
    'mcr_basevad'    : 'voutdir="{outroot}/{{modname}}" outpath="{{voutdir}}/{{e_srcname}}/{{e_srcfile}}" overwrite=No',
    'mcr_labels_vad' : 'labels-attr="vad_labels" path-attr="vout_path"',
    'mcr_labels_gt'  : 'labels-attr=gt_labels path-attr=gt_path',
    'mcr_compare'    : 'sep-sources=Yes inputs=vad_labels,gt_labels',
    'mcr_matlab'    : 'mcr_basevad voutdir="{outroot}/matlab/{{engine}}_{{script}}" ' \
                      'bin=matlab mopts="-nojvm, -nosplash" ' \
                      'scriptdir={binroot}/matlab fread=600 filecount=128 args=""',

    # Default modules' configurations
    'dft_iosingled' : 'iosingled mcr_io k=1',
    'dft_iostamps'  : 'iostamps mcr_io re="" split=""',
    'dft_iogapless' : 'iogapless mcr_io',
    'dft_matlab'    : 'vadmatlab mcr_matlab fread=600 filecount=128 args=""',
    # DB modules
    'nist05' : 'dbnist05 source-name=NIST05 dataset="" re="" ' \
               'source-dir="{dbroot}/NIST05/DATA" gt-dir="{dbroot}/NIST05/GT/ASR"',
    'nist08' : 'dbnist08 source-name=NIST08 dataset="" dataunits="" channels="" re="" ' \
               ' source-dir="{dbroot}/NIST08/DATA/" gt-dir="{dbroot}/NIST08/GT/"',    
    'aurora' : 'dbaurora source-name=Aurora2 dataset=TEST env=1,2,3,4 snr=C,20,15,10,5,0,-5 re="" ' \
               'source-dir="{dbroot}/AURORA2/{{dataset}}/DATA" ' \
               'gt-dir="{dbroot}/AURORA2/{{dataset}}/GT" ',
    #IO modules
    'isingle'   : 'dft_iosingled mcr_labels_gt action=read ', 
    'ivsingle'  : 'dft_iosingled mcr_labels_vad action=read', 
    'igapless'  : 'dft_iogapless mcr_labels_gt action=read',
    'ivgapless' : 'dft_iogapless mcr_labels_vad action=read',
    'idummy'    : 'genericiomodulebase mcr_io mcr_labels_gt action=read',
    'odummy'    : 'genericiomodulebase mcr_io mcr_labels_gt action=write',
    'osingle'   : 'dft_iosingled mcr_labels_gt action=write',
    'ogapless'  : 'dft_iogapless mcr_labels_gt action=write',
    'ostamps'   : 'dft_iostamps mcr_labels_gt action=write',
    'ovstamps'  : 'dft_iostamps mcr_labels_vad action=write', 
    'ovsingle'  : 'dft_iosingled mcr_labels_vad action=write',
    'ovgapless' : 'dft_iogapless mcr_labels_vad action=write',
    # DB->IO aliases
    'inist'     : 'dft_iostamps re=(?P<ss>\d.+) split=" " action=read labels-attr=gt_labels path-attr=gt_path ',
    'ibusstop'  : 'dft_iostamps re=(?P<mm>\d+):(?P<ss>\d+) split=" " action=read labels-attr=gt_labels path-attr=gt_path ',
    'ilabra'    : 'dft_iostamps re=(?P<hh>\d+):(?P<mm>\d+):(?P<ss>\d+) split=" " ' \
                  'action=read labels-attr=gt_labels path-attr=gt_path ',

    # VAD->IO aliases
    'ig729'     : 'ivsingle frame-len=0.01',
    'iamr'      : 'ivsingle frame-len=0.02',
    'isilk'     : 'ivgapless frame-len=0.02',

    # VAD modulse
    'g729'     : 'vadg729 mcr_basevad voutdir="{outroot}/g729" exec-path="{binroot}/g729/g729vad" ',
    'amr1'     : 'vadamr mcr_basevad voutdir="{outroot}/amr1" exec-path="{binroot}/amr/amr1" ',
    'amr2'     : 'vadamr mcr_basevad voutdir="{outroot}/amr2" exec-path="{binroot}/amr/amr2" ',
    'afe'      : 'vadafe mcr_basevad voutdir="{outroot}/afe" exec-path="{binroot}/afe/afe" ',
    'silk'     : 'vadsilk mcr_basevad voutdir="{outroot}/silk" exec-path="{binroot}/silk/silkvad" ', 
    'matlab'   : 'dft_matlab engine=vad',
    'svmtrain' : 'vadmatlabsvm mcr_matlab conf_framelen engine=svm script=train ' \
                 'outpath="{{voutdir}}/{{e_srcname}}/{{e_srcfile}}.mat"',
    'svmtest'  : 'vadmatlabsvm mcr_matlab conf_framelen engine=svm script=test ' \
                 'outpath="{{voutdir}}/{{e_srcname}}/{{e_srcfile}}"',

    # Other modules
    'info'       : 'modinfo attr="__info__"',
    'cat'        : 'modcat gt=yes source=yes',
    'split'      : 'modsplit gt=yes source=yes length=60 overwrite=No ' \
                   'out-source-path="{outroot}/split/{{e_srcname}}/{{e_srcfile}}.{{counter}}" ' \
                   'out-gt-path="{outroot}/split/{{e_srcname}}/GT/{{e_srcfile}}.{{counter}}"', 
    'edit'       : 'modedit attr="" value="{{attr}}" from_attr="" to_attr=""',
    'confusion'  : 'modconfusion mcr_compare fscore-b=1',
    'agreement'  : 'modagreement mcr_compare re=""', 
    'multivad'   : 'modmultivad out-labels-attr="vad_labels" max-diff-rate=0.005',
    'vurate'     : 'modvurate labels-attr=gt_labels'
}
