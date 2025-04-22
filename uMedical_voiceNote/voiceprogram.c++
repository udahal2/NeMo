//voice_to_speak ="The patient has been complaining of chest pain for the past week. ECG shows irregular rhythm. Prescribed low dose beta-blocker. Recommended follow-up in 5 days."

// write a program in c++ ; that generates a clearly audible whose frequency is 18KHz and loudness is 2dB.
// the note should be as shown in variable voice_to_speak.


// The active selection contains a comment in a C++ file that outlines a task to be implemented. The first line of the comment defines a variable, `voice_to_speak`, which holds a string describing a medical note. This note includes details about a patient's symptoms, diagnostic findings, prescribed medication, and follow-up recommendations. While the variable is commented out, it serves as an example of the content that the program will need to process or output.

// The second part of the comment specifies the requirements for the program to be written. The program's goal is to generate a sound that is clearly audible, with a frequency of 18 kHz and a loudness of 2 dB. Additionally, the sound should convey the content of the `voice_to_speak` variable, meaning the program must synthesize speech or audio that communicates the text message.

// This task involves two main challenges: (1) generating a sound with the specified frequency and loudness, and (2) converting the text into audible speech. The first challenge requires knowledge of audio signal generation, possibly using libraries or APIs that allow precise control over sound properties. The second challenge involves text-to-speech (TTS) synthesis, which can be implemented using libraries like Google's TTS API, Microsoft's Speech SDK, or open-source alternatives like eSpeak. Combining these two aspects ensures the program meets the requirements outlined in the comment.

#include <iostream>
#include <windows.h>
#include <sapi.h>  // SAPI for Text-to-Speech
#include <cmath>
#include <thread>
#include <chrono>

// Generate 18kHz tone for 3 seconds at ~2dB
void generateTone() {
    Beep(18000, 3000);  // Beep(frequency, duration_ms)
    // Note: Beep doesn't allow setting dB directly; volume is controlled system-wide.
}

void speakText(const std::wstring& text) {
    ISpVoice* pVoice = nullptr;

    if (FAILED(::CoInitialize(nullptr))) {
        std::cerr << "Failed to initialize COM." << std::endl;
        return;
    }

    HRESULT hr = CoCreateInstance(CLSID_SpVoice, nullptr, CLSCTX_ALL, IID_ISpVoice, (void**)&pVoice);

    if (SUCCEEDED(hr)) {
        pVoice->Speak(text.c_str(), SPF_IS_XML, nullptr);
        pVoice->Release();
    } else {
        std::cerr << "Failed to create SAPI voice instance." << std::endl;
    }

    ::CoUninitialize();
}

int main() {
    std::wstring voice_to_speak = L"The patient has been complaining of chest pain for the past week. ECG shows irregular rhythm. Prescribed low dose beta-blocker. Recommended follow-up in 5 days.";

    std::cout << "Generating 18kHz tone..." << std::endl;
    generateTone();

    std::cout << "Speaking medical note..." << std::endl;
    speakText(voice_to_speak);

    return 0;
}
