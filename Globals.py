
from itertools import chain


session_static_json = {
    "sessionRequestData": {
        "audioMode": 2,
        "remoteControllersBitmap": 0,
        "sdrHdrMode": 0,
        "networkTestSessionId": None,
        "availableSupportedControllers": [],
        "clientVersion": "26.0", # Update this to the latest version
        "deviceHashId": "9fc511bc-a4fc-4351-b401-e4fbbb523c6f",
        "internalTitle": None,
        "clientPlatformName": "browser",
        "metaData": [
            {"key": "isAppLaunchEnabled", "value": "True"},
            {"key": "SubSessionId", "value": "45af1033-8578-4376-91ed" "-b1b724489bd8"},
            {"key": "wssignaling", "value": "1"},
            {"key": "GSStreamerType", "value": "WebRTC"},
            {"key": "networkType", "value": "Unknown"},
            {"key": "ClientImeSupport", "value": "0"},
            {
                "key": "clientPhysicalResolution",
                "value": '{"horizontalPixels":1920,' '"verticalPixels":1080}',
            },
            {"key": "surroundAudioInfo", "value": "2"},
        ],
        "surroundAudioInfo": 0,
        "clientTimezoneOffset": 7200000,
        "clientIdentification": "GFN-PC",
        "parentSessionId": None,
        "appId": "100163111",
        "streamerVersion": 1,
        "clientRequestMonitorSettings": [
            {"heightInPixels": 1080, "framesPerSecond": 60, "widthInPixels": 1920}
        ],
        "appLaunchMode": 1,
        "sdkVersion": "1.0",
        "enchancedStreamMode": 1,
        "useOps": True,
        "clientDisplayHdrCapabilities": None,
        "accountLinked": False,
        "partnerCustomData": "",
        "enablePersistingInGameSettings": False,
        "secureRTSPSupported": False,
    }
}

# =============================
#           GFN Servers
# =============================

# Europe
EU_Northeast_FREE = [
    "NP-AMS-02",
    "NP-AMS-03",
    "NP-AMS-04",
    "NP-PAR-02",
    "NP-PAR-03",
    "NP-LON-03",
    "NP-LON-04",
]
EU_Central_FREE = [
    "NP-FRK-04",
    "NP-FRK-05",
]
EU_Southwest_FREE = [
    "NP-PAR-02",
    "NP-PAR-03",
]
EU_West_FREE = [
    "NP-LON-03",
    "NP-LON-04",
]
EU_Northwest_FREE = [
    "NP-STH-02",
]
EU_Southeast_FREE = [
    "NP-SOF-01",
]


# America
US_Central_FREE = [
    "NP-DAL-02",
    "NP-DAL-03",
]

US_East_FREE = [
    "NP-ASH-03",
]

US_Midwest_FREE = [
    "NP-CHI-03",
]

US_Northeast_FREE = [
    "NP-NWK-02",
]

US_Northwest_FREE = [
    "NP-PDX-02",
]

US_South_FREE = [
    "NP-ATL-02",
]

US_Southeast_FREE = [
    "NP-MIA-02",
]

US_Southwest_FREE = [
    "NP-LAX-02",
]

US_Mountain_FREE = [
    "NP-PHX-01",
]

US_West_FREE = [
    "NP-SJC6-02",
]


# CA
CA_East_FREE = [
    "NP-MON-01",
]

# Combined Lists
EU_FREE_LIST = list(
    chain(
        EU_Northeast_FREE,
        EU_Central_FREE,
        EU_Southwest_FREE,
        EU_West_FREE,
        EU_Northwest_FREE,
        EU_Southeast_FREE,
    )
)


US_FREE_LIST = list(
    chain(
        US_Central_FREE,
        US_East_FREE,
        US_Midwest_FREE,
        US_Northeast_FREE,
        US_Northwest_FREE,
        US_South_FREE,
        US_Southeast_FREE,
        US_Southwest_FREE,
        US_Mountain_FREE,
        US_West_FREE,
    )
)

CA_FREE_LIST = list(chain(CA_East_FREE))

# =============================
