# Required constants

# modules PATH
PATH = ['./modules',
        ]

# Macros 
ROOT = '..'                 # {root}
BINDIR = ROOT + '/bin'      # {bindir}
OUTDIR = ROOT + '/output'   # {outdir}
DBDIR = ROOT + '/databases' # {dbdir}
IFRAMELEN = 0.08            # {iframelen}, input frame length
OFRAMELEN = 0.04            # {oframelen}, output frame length

MACROS = {   
    'nist' : 'dbnist root="{dbdir}/NIST" source-dir=DATA gt-dir=GT',
    'inist' : 'iostamps re=(?P<ss>\d.+) split=" " action=read frame-len={iframelen}',
    'isingle' : 'iosingled action=read frame-len={iframelen} k=1', 
    'ostamps' : 'iostamps re="" split="" action=write frame-len={oframelen}', 
    'osingle' : 'iosingled action=write frame-len={oframelen}',

    # vad modules
    'g729' : 'vadg729 voutdir="{outdir}/g729" exec-path="{bindir}/g729/g729vad" ',
    'amr1' : 'vadamr voutdir="{outdir}/amr1" exec-path="{bindir}/amr/amr1" ',
    'amr2' : 'vadamr voutdir="{outdir}/amr2" exec-path="{bindir}/amr/amr2" ',
    'matlab' : 'vadmatlab voutdir="{outdir}/matlab" bin=matlab mopts="-nojvm, -nosplash" ' \
               'scriptdir={bindir}/matlab engine=vad script="" fread=600 filecount=128 args=""',
    'mtrain' : 'matlab engine=train',
    'mtest' : 'matlab engine=test',

    'dbcat': 'cat outdir="{outdir}"',
}

format_args = {
    'root' : ROOT, 
    'bindir' : BINDIR,
    'outdir' : OUTDIR, 
    'dbdir' : DBDIR, 
    'iframelen' : IFRAMELEN, 
    'oframelen' : OFRAMELEN,
}
