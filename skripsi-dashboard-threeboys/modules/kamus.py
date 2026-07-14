KAMUS_BARANG = {
    'oli mpx 1 0.8'      : 'oli mpx 1 0.8l',
    'oli mpx 2 0.8'      : 'oli mpx 2 0.8l',
    'oli mpx 2 0.65 l'   : 'oli mpx 2 0.65l',
    'air radiator / coolant biasa'    : 'air radiator biasa',
    'air radiator / coolant honda'    : 'air radiator honda',
    'air radiator / cooolant yamalube': 'air radiator yamalube',
    'aki gtz 5 s gs' : 'aki gtz 5s gs',
    'aki gtz 6 v tsp': 'aki gtz 6v tsp',
    'aki gtz 7v tsp' : 'aki gtz 7s tsp',
    'asbes.paking knalpot' : 'asbes / paking knalpot',
    'oli samping motul' : 'oli samping motul 2t',
    'stelan rantai supra (per biji0)' : 'stelan rantai supra (per biji)'
}

KAMUS_SERVIS = {
    'service' : 'jasa service',
    'jasa' : 'jasa service',
    'jasa perbaikan' : 'jasa service',
    'jasa perbaikan / jasa pasang barang' : 'jasa pasang sparepart',
    'pasang sparepat' : 'jasa pasang sparepart',
    'jasa pasang barang' : 'jasa pasang sparepart',
    'cas / charger aki' : 'cas / strom aki',
    'service cvt beat. scoopy. genio. dll' : 'servis cvt matic',
    'servis cvt ( beat. scoopi. genio.mio. fino. dll )' : 'servis cvt matic',
    'servis cvt ( vario. nmax. aerox. pcx. dll )' : 'servis cvt matic',
    'service throttle body / injekction beat. scoopy. genio. dll' : 'servis throttle body',
    'servis trotel body ( vario 125. vario 150. beat. scopy. mio j. fi )' : 'servis throttle body',
    'servis karbu (beat.vario.mio.supra.dll)' : 'servis karbu',
    'servis karbu (jupiter.fu.megapro.dll)' : 'servis karbu'
}

def get_semua_kamus():
    return {**KAMUS_BARANG, **KAMUS_SERVIS}