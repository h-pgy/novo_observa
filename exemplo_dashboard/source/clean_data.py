


class FiltroRegionalizacao:

    def identificar_distrito(self, val):
        
        reg = val.get('Regiao', '')
        return 'distrito' in reg.lower()

    def identificar_subprefeitura(self, val):
        
        reg = val.get('Regiao', '')
        return 'subprefeitura' in reg.lower() 

    def identificar_municipio(self, val):
        
        reg = val.get('Regiao', '')
        return 'município' in reg.lower()   
        
        
    def region_distrito(self, values):
        
        return [val for val in values if self.identificar_distrito(val)]

    def region_subs(self, values):
        
        return [val for val in values if self.identificar_subprefeitura(val)]

    def region_municip(self, values):

        return [val for val in values if self.identificar_municipio(val)]

    def filter_data(self, values):


        distritos = self.region_distrito(values)
        subs = self.region_subs(values)
        mun = self.region_municip(values)
        outros = [val for val in values
            if val not in distritos and 
            val not in subs and
            val not in mun]

        return {
            'distritos' : distritos,
            'subprefeituras' : subs,
            'municipio' : mun,
            'outros' : outros 
        }

    def __call__(self, values):

        return self.filter_data(values)

class CleanData:

    def __init__(self):

        self.filtrar_regiao = FiltroRegionalizacao()

    def clean_distrito(self, regiao):

        regiao = regiao.lower()
        regiao = regiao.replace('(distrito)', '')

        return regiao

    def clean_subs(self, regiao):

        regiao = regiao.lower()
        regiao = regiao.replace('(subprefeitura)', '')

        return regiao

    def clean_municip(self, regiao):

        regiao = regiao.lower()
        regiao = regiao.replace('(município)', '')

        return regiao

    def clean_regiao(self, indi, tp_regiao):

        if indi.get('Regiao') is None:
            return None
        if tp_regiao == 'distritos':
            return self.clean_distrito(indi['Regiao'])
        if tp_regiao == 'subprefeituras':
            return self.clean_subs(indi['Regiao'])
        if tp_regiao == 'municipio':
            return self.clean_municip(indi['Regiao'])

        return indi['Regiao']

    def clean_result(self, indi):

        result = indi['ResultadoIndicadorStr']

        result = result.replace('.', '')
        result = result.replace(',', '.')

        return float(result)
    
    def clean_periodo(self, indi):

        periodo = indi.get('Periodo')

        try:
            return int(periodo)
        except ValueError:
            return periodo

    def clean_value(self, indi, tp_regiao):

        return {
        'periodo' : self.clean_periodo(indi),
        'valor' : self.clean_result(indi),
        'regiao' : self.clean_regiao(indi, tp_regiao)
        }


    def clean_values(self, values):

        cleaned = {}
        regionalizado = self.filtrar_regiao(values)
        for tp_regiao, values in regionalizado.items():
            if tp_regiao not in cleaned:
                cleaned[tp_regiao] = []
            for val in values:
                cleaned[tp_regiao].append(self.clean_value(val, tp_regiao))

        return cleaned

    def clean_indicador(self, indicador):

        data = indicador.pop('data')

        cleaned = self.clean_values(data)

        indicador['data'] = cleaned

        return indicador

    def __call__(self, indicador):

        return self.clean_indicador(indicador)
                




