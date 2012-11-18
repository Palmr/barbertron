extern "C" 
{
#include <z_libpd.h>
}

#include <deque>
#include <fstream>
#include <iostream>
#include <string>
#include <sndfile.h>
#include <cmath>

void pd_printCallback(const char *s) {
  std::cout << s;
}

void pd_noteOnCallback(int ch, int pitch, int vel) {
  std::cout << ch << ", " <<  pitch << ", " << vel << std::endl;
}

struct NoteOn {
  float time;
  int pitch;
  int velocity;
};

int readControlFile(const std::string &controlFilePath, std::deque<NoteOn> & noteOnSignals)
{
  std::ifstream inFile(controlFilePath.c_str());

  NoteOn noteOn;
  while( inFile >> noteOn.time >> noteOn.pitch >> noteOn.velocity )
  {
    noteOnSignals.push_back(noteOn);
  }

  return 0;
}

int main(int argc, char *argv[])
{
  std::cout << "Hello world" << std::endl;

  if (argc < 5) {
    std::cerr << "Usage: " << argv[0] << " patch.pd audio.wav controlData.txt" << std::endl;
    return -1;
  }

  std::string pdPatch(argv[1]);
  std::string audioInput(argv[2]);
  std::string controlFile(argv[3]);
  std::string audioOutput(argv[4]);

  std::cout << "USING PD PATCH: " << pdPatch << std::endl;
  std::cout << "LOADING AUDIO FILE: " << audioInput << std::endl;
  std::cout << "LOADING BARBERISM INSTRUCTIONS: " << controlFile << std::endl;
  std::cout << "WRITING TO AUDIO FILE: " << audioOutput << std::endl;

  std::deque<NoteOn> noteOnSignals;
  readControlFile(controlFile, noteOnSignals);

  size_t dirCharIndex = pdPatch.rfind('/');
  if (dirCharIndex == pdPatch.npos)
  {
    std::cerr << "Invalid pdPatch path" << std::endl;
    return -1;
  }
  std::string pdPatchDir = pdPatch.substr(0, dirCharIndex);
  std::string pdPatchFile = pdPatch.substr(dirCharIndex+1);

  SNDFILE *audioInputFileHandle;
  SF_INFO inputFormat;
  audioInputFileHandle = sf_open(audioInput.c_str(), SFM_READ, &inputFormat);
  if (NULL == audioInputFileHandle)
  {
    std::cerr << "Failed to load audio file." << std::endl;
    std::cerr << sf_strerror(NULL) << std::endl;
    return -1;
  }
  int sampleRate = inputFormat.samplerate;
  long frameCount = inputFormat.frames;
  int channels = inputFormat.channels;

  SF_INFO outputFormat;
  outputFormat.samplerate = sampleRate;
  outputFormat.format = SF_FORMAT_WAV | SF_FORMAT_PCM_16;
  outputFormat.channels = channels;
  SNDFILE *audioOutputFileHandle = sf_open(audioOutput.c_str(), SFM_WRITE, &outputFormat);
  if (NULL == audioOutputFileHandle)
  {
    std::cerr << "Failed to open output audio file for writing." << std::endl;
    std::cerr << sf_strerror(NULL) << std::endl;
    return -1;
  }

  std::cout << "SAMPLE RATE: " << sampleRate << std::endl;
  std::cout << "FRAME COUNT: " << frameCount << std::endl;
  std::cout << "CHANNEL COUNT: " << channels << std::endl;

  if (channels != 1)
  {
    std::cerr << "Multiple channels are not supported" << std::endl;
    return -1;
  }

  float *audioInData = new float[frameCount*channels];
  int samplesRead = sf_readf_float(audioInputFileHandle, audioInData, frameCount);

  std::cout << "Successfully read " << samplesRead << " frames into temp memory" << std::endl;

  if (sf_close(audioInputFileHandle) != 0)
  {
    std::cerr << "Error closing file" << std::endl;
  }

  std::cout << "INITIALISE PURE DATA" << std::endl;
  libpd_printhook = (t_libpd_printhook) pd_printCallback;
  libpd_noteonhook = (t_libpd_noteonhook) pd_noteOnCallback;
  libpd_init();
  libpd_init_audio(1, 1, sampleRate);
  const int ticks = 4;
  long blockSize = libpd_blocksize() * ticks;
  float inbuf[blockSize], outbuf[blockSize];

  // compute audio    [; pd dsp 1(
  libpd_start_message(1); // one entry in list
  libpd_add_float(1.0f);
  libpd_finish_message("pd", "dsp");

  // open patch       [; pd open file folder(
  libpd_openfile(pdPatchFile.c_str(), pdPatchDir.c_str());
  int midiChannel = 1;
  int pitch = 67;
  int velocity = 100;
  if (0 != libpd_noteon(midiChannel, pitch, velocity))
  {
    std::cout << "Failed to send MIDI data to PD." << std::endl;
  }
  pitch = 76;
  if (0 != libpd_noteon(midiChannel, pitch, velocity))
  {
    std::cout << "Failed to send MIDI data to PD." << std::endl;
  }

  std::cout << "PROCESSING DATA" << std::endl;
  int frameIndex = 0;
  std::cout << "TOTAL SAMPLES : " << frameCount << std::endl;
  while (frameIndex < frameCount * channels / blockSize)
  {
    std::cout << "FRAME : " << frameIndex << std::endl;
    long thisBlockFrames = std::min(blockSize, frameCount - frameIndex * blockSize);

    // Fill PD input buffer
    for (int i = 0; i < thisBlockFrames; ++i)
    {
      inbuf[i] = audioInData[frameIndex * blockSize + i];
    }

    if (noteOnSignals.size() && noteOnSignals[0].time < frameIndex * blockSize / (float)sampleRate)
    {
      const NoteOn &noteOn = noteOnSignals[0];
      if (0 != libpd_noteon(midiChannel, noteOn.pitch, noteOn.velocity))
      {
        std::cout << "Failed to send MIDI data to PD." << std::endl;
      }
      else
      {
        std::cout << "Sent MIDI data to PD: " << noteOn.pitch << " " << noteOn.velocity << std::endl;
      }
      noteOnSignals.pop_front();

    }

    libpd_process_float(ticks, inbuf, outbuf);

    // use outbuf here
    sf_count_t framesWritten = sf_writef_float(audioOutputFileHandle, outbuf, thisBlockFrames) ;
    float max = 0;
    for (int i = 0; i < thisBlockFrames; ++i)
    {
      max = std::max(max, outbuf[i]);
    }
    std::cout << "Wrote " << framesWritten << " frames" << ", max " << max << std::endl;
    frameIndex ++;
  }
  std::cout << "FINISHED, CLEANING UP" << std::endl;
  delete[] audioInData;
  if (sf_close(audioOutputFileHandle) != 0)
  {
    std::cerr << "Error closing output file" << std::endl;
  }

  return 0;
}
