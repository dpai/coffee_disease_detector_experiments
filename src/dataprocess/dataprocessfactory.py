from src.dataprocess.siameseprocessor import SiameseDataProcessor

_availableProcTypes = {
    SiameseDataProcessor._processName : SiameseDataProcessor._className
}

def dataProcessorFactory(params):
    if params.build_data in _availableProcTypes.keys():
        dataprocessor = eval(_availableProcTypes[params.build_data])(params.data_path)
                                            
    return dataprocessor
    