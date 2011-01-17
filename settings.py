# Required constants
PATH = ['/home/zaur/Documents/Study/vadpy2/src/modules', 
        '/media/devel/thesis/vadpy2/src/modules'
        ]

ROOT = '/home/zaur/Documents/Study/vadpy2'
#ROOT = '/media/devel/thesis/vadpy2'
BINDIR = ROOT + '/bin'
OUTDIR = ROOT + '/output'

# Macros 
MACROS = {   
    'nist' : 'dbnist root="{root}/databases/NIST" source-dir=DATA gt-dir=GT',
    #'ionist' : 'iostamps re=(?P<ss>\d.+) split=" " action=read frame-len=0.008', 
    'ionist' : 'iosingled action=read frame-len=0.008 k=1', 
   
    # vad modules
    'g729' : 'vadg729 outdir="{outdir}/g729" exec-path="{bindir}/g729/g729vad" ',
    'matlab' : 'vadmatlab outdir="{outdir}/matlab" bin=matlab mopts="-nojvm, -nosplash" ' \
               'scriptdir={bindir}/matlab engine=vad script="" fread=600 filecount=128 args=""',
    'mtrain' : 'matlab engine=train',
    'mtest' : 'matlab engine=test',

    'dbcat': 'cat outdir="{outdir}"'
}
