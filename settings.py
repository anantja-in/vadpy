import os
import getpass

# ROOT is the path to VADpy directory
# For example ROOT = '/home/user/.vadpy/'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# modules' PATH
PATH = [os.path.join(ROOT, 'src/modules'),
        ]

# The format_args are used in VADpy macros as following:
# 'voutdir="{outroot}/vad" '
# here, {outroot} is defined in format_args
format_args = {
    'root' : ROOT,
    'binroot' : os.path.join(ROOT, 'bin'),
    'outroot' : os.path.join(ROOT, 'output', getpass.getuser()),
    'dbroot' :  os.path.join(ROOT, 'databases')
}

MACROS = {
    # configuration values
    'conf_framelen'  : 'frame-len=0.01',

    # macros
    'mcr_io'         : 'conf_framelen path-attr=""',
    'mcr_basevad'    : 'voutdir="{outroot}/{{modname}}" ' \
                       'outpath="{{voutdir}}/{{e_srcname}}/{{e_srcfile}}" overwrite=No',
    'mcr_labels_vad' : 'labels-attr="vad_labels" path-attr="vout_path"',
    'mcr_labels_gt'  : 'labels-attr=gt_labels path-attr=gt_path',
    'mcr_compute'    : 'print=Yes',
    'mcr_matlab'     : 'mcr_basevad voutdir="{outroot}/matlab/{{engine}}_{{script}}" ' \
                       'bin=matlab mopts="-nojvm, -nosplash" ' \
                       'scriptdir={binroot}/matlab fread=600 filecount=128 Argos=""',

    # Default modules' configurations
    'dft_iosingled' : 'iosingled mcr_io k=1',
    'dft_iostamps'  : 'iostamps mcr_io re="" split=""',
    'dft_iogapless' : 'iogapless mcr_io',
    'dft_matlab'    : 'vadmatlab mcr_matlab fread=600 filecount=128 args=""',

    # DB modules
    'aurora'  : ('dbaurora source-name=Aurora2/{{dataset}} '
                 'dataset=TEST env=1,2,3,4 snr=C,20,15,10,5,0,-5 re="" '
                 'source-dir="{dbroot}/AURORA2/{{dataset}}/DATA" '
                 'gt-dir="{dbroot}/AURORA2/{{dataset}}/GT" '),
    'nist05'  : ('dbnist05 source-name=NIST05 re="" '
                'source-dir="{dbroot}/NIST05/{{dataset}}/DATA" dataset=TEST '
                'gt-dir="{dbroot}/NIST05/{{dataset}}/GT"'),
    'busstop' : ('dbquick source-name=busstop/{{dataset}} '
                 'dataset="TEST" flags=8000hz,le,16bps re="" '
                 'gt-dir="{dbroot}/busstop/{{dataset}}/GT" '
                 'source-dir="{dbroot}/busstop/{{dataset}}/DATA" '),
    'test'    : 'dbquick source-name=testdb dataset="" flags=8000hz,le,16bps re="" ' \
                'gt-dir="{dbroot}/TESTDB/GT" source-dir="{dbroot}/TESTDB/DATA/{{dataset}}" ',
    'labra'  :  'dbquick source-name=labra dataset="" flags=8000hz,le,16bps re="" ' \
                'gt-dir={dbroot}/LABRA/GT source-dir={dbroot}/LABRA/DATA/ ',
    # 'nist08' : 'dbnist08 source-name=NIST08 dataset="" dataunits="" channels="" re="" ' \
    #            ' source-dir="{dbroot}/NIST08/DATA/" gt-dir="{dbroot}/NIST08/GT/"',

    #IO modules
    'isingle'   : 'dft_iosingled mcr_labels_gt action=read',
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
    'iaurora'   : 'igapless frame-len=0.01',
    'inist'     : 'igapless frame-len=0.01',
    'ilabra'    : 'dft_iostamps re=(?P<hh>\d+):(?P<mm>\d+):(?P<ss>\d+) split=" " ' \
                  'action=read labels-attr=gt_labels path-attr=gt_path frame-len=1',
    'ibusstop'  : 'igapless frame-len=1',
    'itest'     : 'dft_iostamps re=(?P<ss>\d.+) split=" " action=read ' \
                  'labels-attr=gt_labels path-attr=gt_path frame-len=0.01',

    # VAD->IO aliases
    'ig729'     : 'ivgapless frame-len=0.01',
    'iamr'      : 'ivgapless frame-len=0.02',
    'isilk'     : 'ivgapless frame-len=0.02',
    'iafe'      : 'ivgapless frame-len=0.01',
    'imatlab'   : 'ivgapless frame-len=0.01',
    'ienergy'   : 'imatlab',
    'ientropy'  : 'imatlab',
    'isvm'      : 'ivgapless',

    # VAD modulse
    'g729'      : 'vadg729 mcr_basevad voutdir="{outroot}/g729" exec-path="{binroot}/g729/g729vad" ',
    'amr1'      : 'vadamr mcr_basevad voutdir="{outroot}/amr1" exec-path="{binroot}/amr/amr1" ',
    'amr2'      : 'vadamr mcr_basevad voutdir="{outroot}/amr2" exec-path="{binroot}/amr/amr2" ',
    'afe'       : 'vadafe mcr_basevad voutdir="{outroot}/afe" exec-path="{binroot}/afe/afe" ',
    'silk'      : 'vadsilk mcr_basevad voutdir="{outroot}/silk" exec-path="{binroot}/silk/silkvad" ',
    'svmtrain'  : 'vadmatlabsvm mcr_matlab conf_framelen engine=svm script=train ' \
                  'outpath="{{voutdir}}/{{e_srcname}}/{{e_srcfile}}.mat"',
    'svmtest'   : 'vadmatlabsvm mcr_matlab conf_framelen engine=svm script=test ' \
                  'outpath="{{voutdir}}/{{e_srcname}}/{{e_srcfile}}"',
    'energy.m'  : 'dft_matlab engine=vad script=energy',
    'entropy.m' : 'dft_matlab engine=vad script=entropy',
    'stat.m'    : 'dft_matlab engine=vad script=logmmse_SPU2 args="1" ' \
                  'voutdir="{outroot}/matlab/{{engine}}_stat{{args}}"',
    'stat1.m'   : 'stat.m args="1"',
    'stat2.m'   : 'stat.m args="2"',
    'stat3.m'   : 'stat.m args="3"',
    'stat4.m'   : 'stat.m args="4"',

    # Decision modules
    'mcr_fusion' : 'modfusion output=vad_labels max-diff-rate=0.005 margs="" ctx-size=0',
    'mfusion'    : 'mcr_fusion method=majority',
    'bfusion'    : 'mcr_fusion margs=gt_labels method=bayes',
    'hfusion'    : 'mcr_fusion margs=gt_labels method=simplehist',

    # Computation modules
    'sr'         : 'modsr mcr_compute inputs=gt_labels',
    'histogram'  : 'modfusionhistogram mcr_compute print=No',
    'chistogram' : 'modsourcehistogram mcr_compute',
    'confusion'  : 'modconfusion mcr_compute inputs=gt_labels,vad_labels ctx-size=0',
    'correlation': 'modcorrelation mcr_compute',

    # Other modules
    'info'       : 'modinfo attr="__summary__"',
    'concat'     : 'modconcat gt=yes source=yes',
    'split'      : 'modsplit gt=yes source=yes length=60 overwrite=No ' \
                   'out-source-path="{outroot}/split/{{e_srcname}}/{{e_srcfile}}.{{counter}}" ' \
                   'out-gt-path="{outroot}/split/{{e_srcname}}/GT/{{e_srcfile}}.{{counter}}"',
    'edit'       : 'modedit attr="" value="{{attr}}" copy-from="" copy-to=""',
    'extract'    : 'modextract mode=speech out-path="{outroot}/fusion/{{e_srcfile}}"',
    'vurate'     : 'modvurate labels-attr=gt_labels',
    'pipe'       : 'modpipeline ',
}

