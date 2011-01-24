# Required constants

# modules PATH
PATH = ['./modules',
        ]


# Macros 
ROOT = '..' # {root}
BINDIR = ROOT + '/bin'      # {bindir}
OUTDIR = ROOT + '/output'   # {outdir}
DBDIR = ROOT + '/databases' # {dbdir}
FRAMELEN = 0.08             # {settings}

MACROS = {   
    'nist' : 'dbnist root="{dbdir}/NIST" source-dir=DATA gt-dir=GT',
    'inist' : 'iosingled action=read frame-len={framelen} k=1', 
    'ostamps' : 'iostamps re="" split="" action=write frame-len={framelen}', 
    'osingle' : 'iosingled action=write frame-len={framelen}',

    # vad modules
    'g729' : 'vadg729 outdir="{outdir}/g729" exec-path="{bindir}/g729/g729vad" ',
    'matlab' : 'vadmatlab outdir="{outdir}/matlab" bin=matlab mopts="-nojvm, -nosplash" ' \
               'scriptdir={bindir}/matlab engine=vad script="" fread=600 filecount=128 args=""',
    'mtrain' : 'matlab engine=train',
    'mtest' : 'matlab engine=test',

    'dbcat': 'cat outdir="{outdir}"',
}
