from .classes.AD_BatchImageLoadFromDir import AD_BatchImageLoadFromDir, N_CLASS_MAPPINGS as BATCH_CLASS_MAPPINGS, N_DISPLAY_NAME_MAPPINGS as BATCH_DISPLAY_MAPPINGS
from .classes.AD_DeleteLocalAny import AD_DeleteLocalAny, N_CLASS_MAPPINGS as DELETE_CLASS_MAPPINGS, N_DISPLAY_NAME_MAPPINGS as DELETE_DISPLAY_MAPPINGS
from .classes.AD_TextListToString import AD_TextListToString, N_CLASS_MAPPINGS as TEXT_CLASS_MAPPINGS, N_DISPLAY_NAME_MAPPINGS as TEXT_DISPLAY_MAPPINGS
from .classes.AD_AnyFileList import AD_AnyFileList, N_CLASS_MAPPINGS as ANY_CLASS_MAPPINGS, N_DISPLAY_NAME_MAPPINGS as ANY_DISPLAY_MAPPINGS
from .classes.AD_ZipSave import AD_ZipSave, N_CLASS_MAPPINGS as ZIP_CLASS_MAPPINGS, N_DISPLAY_NAME_MAPPINGS as ZIP_DISPLAY_MAPPINGS
from .classes.AD_ImageSaver import AD_ImageSaver, N_CLASS_MAPPINGS as IMAGE_SAVER_CLASS_MAPPINGS, N_DISPLAY_NAME_MAPPINGS as IMAGE_SAVER_DISPLAY_MAPPINGS
from .classes.AD_FluxTrainStepMath import AD_FluxTrainStepMath, N_CLASS_MAPPINGS as FLUX_CLASS_MAPPINGS, N_DISPLAY_NAME_MAPPINGS as FLUX_DISPLAY_MAPPINGS
from .classes.AD_TextSaver import AD_TextSaver, N_CLASS_MAPPINGS as TEXT_SAVER_CLASS_MAPPINGS, N_DISPLAY_NAME_MAPPINGS as TEXT_SAVER_DISPLAY_MAPPINGS
from .classes.AD_PromptReplace import AD_PromptReplace, N_CLASS_MAPPINGS as PROMPT_REPLACE_CLASS_MAPPINGS, N_DISPLAY_NAME_MAPPINGS as PROMPT_REPLACE_DISPLAY_MAPPINGS

NODE_CLASS_MAPPINGS = {
    **BATCH_CLASS_MAPPINGS,
    **DELETE_CLASS_MAPPINGS,
    **TEXT_CLASS_MAPPINGS,
    **ANY_CLASS_MAPPINGS,
    **ZIP_CLASS_MAPPINGS,
    **IMAGE_SAVER_CLASS_MAPPINGS,
    **FLUX_CLASS_MAPPINGS,
    **TEXT_SAVER_CLASS_MAPPINGS,
    **PROMPT_REPLACE_CLASS_MAPPINGS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **BATCH_DISPLAY_MAPPINGS,
    **DELETE_DISPLAY_MAPPINGS,
    **TEXT_DISPLAY_MAPPINGS,
    **ANY_DISPLAY_MAPPINGS,
    **ZIP_DISPLAY_MAPPINGS,
    **IMAGE_SAVER_DISPLAY_MAPPINGS,
    **FLUX_DISPLAY_MAPPINGS,
    **TEXT_SAVER_DISPLAY_MAPPINGS,
    **PROMPT_REPLACE_DISPLAY_MAPPINGS
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

