import re
import unicodedata
def text_cleaning(input_string):
    lowercase = input_string.lower()
    remove_link = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)', '', lowercase).replace("&amp;","&")
    remove_bullet = "\n".join([T for T in remove_link.split('\n') if '•' not in T and "baca juga:" not in T])
    remove_accented = unicodedata.normalize('NFKD', remove_bullet).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    remove_parentheses = re.sub("([\(\|]).*?([\)\|])", "\g<1>\g<2>", remove_accented)
    remove_punc = re.sub(r"[^\w\d.\s]+",' ', remove_parentheses)
    remove_num_dot = re.sub(r"(?<=\d)\.|\.(?=\d)|(?<=#)\.","", remove_punc)
    remove_extra_whitespace =  re.sub(r'^\s*|\s\s*', ' ', remove_num_dot)
    return ".".join([s for s in remove_extra_whitespace.strip().split('.') if len(s.strip())>10]).replace("_","")



s = "Fathiyul\tFahmi\nArtificial\tIntelligence\tEngineer\nIndonesia\nArtificial\tIntelligence\tEngineer\twith\t3+\tyears\tof\texperience\tdoing\tend-to-end\tmachine\tlearning\tmodel\tdevelopment\tand\tdeployment.\tCurrent\twork\nmainly\tinvolved\tin\tbuilding\tComputer\tVision\tenabled\tsystems.\nExperience\nComputer\tVision\tEngineer\nKECILIN\n\t·\tJakarta,\tIndonesia\nJul\t2023\t-\tPresent\nAccelerating\nArtificial\tIntelligence\tEngineer\nPT.\tDelameta\tBilano\n\t·\tJakarta,\tIndonesia\nAug\t2020\t-\tJul\t2023\nBuild\tAI\tsolutions\tfrom\tdata\tanalysis,\tmodel\tdevelopment,\tto\tcode\tdeployment\tin\tedge\tdevices\n(Raspberry\tPi,\tNvidia\tJetson,\tOdroid).\tCode\tmainly\tin\tPython\tand\tC++,\tmostly\twith\tTorch,\nOpenCV,\tand\tScikitLearn.\nMainly\tresponsible\tin\tvehicle\tclassification\tsystem,\tcrowd\tanalytics,\toptical\tcharacter\nrecognition,\tand\tface\trecognition\tsystem,\talso\tinvolved\tin\ttraffic\tmonitoring\tsystem.\nOther\tprojects:\nWrite\tin-house\tML\tlibrary\tin\tC.\nGive\ttechnical\tconsultancy\tfor\tDFT-based\tmolecular\tinteraction\tmodeling\tand\tsimulations\tin\nPython\tfor\tmaterial\tengineering.\nTeaching\tAssistant\nInstitut\tTeknologi\tBandung\t(ITB)\n\t·\tBandung,\tJawa\tBarat,"
s = "SQL\nData\tAnalytics\nEducation\nMaster\tof\tScience\t-\tMS,\tFisika/Ilmu\nAlam\nInstitut\tTeknologi\tBandung\t(ITB)\nGelar\tSarjana,\tFisika/Ilmu\tAlam\nInstitut\tTeknologi\tBandung\t(ITB)\nCertificates\nTensorFlow\tDeveloper\tCertificate\nTensorFlow\tCertificate\tProgram\nPython\tfor\tEverybody\tSpecialization\nCoursera\nThe\tBusiness\tIntelligence\tAnalyst\nCourse\t2020\nUdemy\nAwards\n3rd\tPlace\tof\tUBAYA\tInformatics\nLogical\tProgramming\tCompetition\n2013\nUniversitas\tSurabaya\n1st\tPlace\tof\tSchematics\tITS\tNational\nLogic\tCompetition\t2012\nInstitut\tTeknologi\tSepuluh\tNovember\nLanguages\nin\t·\tNative\tSpeaker\nBahasa\tIndonesia\t·\tNative\tSpeaker\nBahasa\tInggris\t·\tProfessional\tWorking\nBahasa\tJepang\t·\tElementary\nLinks\nlinkedin.com\n/in/fathiyul"
a = text_cleaning(s)
print(f"==>> a: {a}")