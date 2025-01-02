from .classes.AD_BatchImageLoadFromDir import AD_BatchImageLoadFromDir
from .classes.AD_DeleteLocalAny import AD_DeleteLocalAny
from .classes.AD_TextListToString import AD_TextListToString
from .classes.AD_AnyFileList import AD_AnyFileList
from .classes.AD_ZipSave import AD_ZipSave
from .classes.AD_ImageSaver import AD_ImageSaver
from .classes.AD_FluxTrainStepMath import AD_FluxTrainStepMath
from .classes.AD_TextSaver import AD_TextSaver
from .classes.AD_PromptReplace import AD_PromptReplace
from .classes.AD_HFDownload import AD_HFDownload
from .classes.AD_CSVReader import AD_CSVReader
from .classes.AD_CSVPromptStyler import AD_CSVPromptStyler
from .classes.AD_TxtToCSVCombiner import AD_TxtToCSVCombiner
from .classes.AD_CSVTranslator import AD_CSVTranslator
from .classes.AD_LoadImageAdvanced import AD_LoadImageAdvanced
from .classes.AD_ImageDrawRectangleSimple import AD_ImageDrawRectangleSimple
from .classes.AD_ImageIndexer import AD_ImageIndexer
from .classes.AD_TextIndexer import AD_TextIndexer

NODE_CLASS_MAPPINGS = {
    "AD_BatchImageLoadFromDir": AD_BatchImageLoadFromDir,
    "AD_DeleteLocalAny": AD_DeleteLocalAny,
    "AD_TextListToString": AD_TextListToString,
    "AD_AnyFileList": AD_AnyFileList,
    "AD_ZipSave": AD_ZipSave,
    "AD_ImageSaver": AD_ImageSaver,
    "AD_FluxTrainStepMath": AD_FluxTrainStepMath,
    "AD_TextSaver": AD_TextSaver,
    "AD_PromptReplace": AD_PromptReplace,
    "AD_HFDownload": AD_HFDownload,
    "AD_CSVReader": AD_CSVReader,
    "AD_CSVPromptStyler": AD_CSVPromptStyler,
    "AD_TxtToCSVCombiner": AD_TxtToCSVCombiner,
    "AD_CSVTranslator": AD_CSVTranslator,
    "AD_LoadImageAdvanced": AD_LoadImageAdvanced,
    "AD_ImageDrawRectangleSimple": AD_ImageDrawRectangleSimple,
    "AD_ImageIndexer": AD_ImageIndexer,
    "AD_TextIndexer": AD_TextIndexer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AD_BatchImageLoadFromDir": "🌻 Batch Image Load From Directory",
    "AD_DeleteLocalAny": "🌻 Delete Local Any",
    "AD_TextListToString": "🌻 Text List To String",
    "AD_AnyFileList": "🌻 Any File List",
    "AD_ZipSave": "🌻 Zip Save",
    "AD_ImageSaver": "🌻 Image Saver",
    "AD_FluxTrainStepMath": "🌻 Flux Train Step Math",
    "AD_TextSaver": "🌻 Text Saver",
    "AD_PromptReplace": "🌻 Prompt Replace",
    "AD_HFDownload": "🌻 Hugging Face Download",
    "AD_CSVReader": "🌻 CSV Reader",
    "AD_CSVPromptStyler": "🌻 CSV Prompt Styler",
    "AD_TxtToCSVCombiner": "🌻 Txt to CSV Combiner",
    "AD_CSVTranslator": "🌻 CSV Translator",
    "AD_LoadImageAdvanced": "🌻 Load Image Advanced",
    "AD_ImageDrawRectangleSimple": "🌻 Draw Simple Rectangle",
    "AD_ImageIndexer": "🌻 Image Indexer",
    "AD_TextIndexer": "🌻 Text Indexer",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

