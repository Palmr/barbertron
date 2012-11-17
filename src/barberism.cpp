extern "C" 
{
#include <z_libpd.h>
}

#include <iostream>

/*
void pdprint(const char *s) {
  printf("%s", s);
}

void pdnoteon(int ch, int pitch, int vel) {
  printf("noteon: %d %d %d\n", ch, pitch, vel);
}
*/

int main(int argc, char *argv[])
{
  std::cout << "Hello world" << std::endl;

  if (argc < 4) {
    std::cerr << "Usage: " << argv[0] << " patch.pd audio.wav controlData.txt" << std::endl;
    return -1;
  }

  std::string pdPatch(argv[1]);
  std::string audioInput(argv[2]);
  std::string controlFile(argv[3]);

  std::cout << "USING PD PATCH: " << pdPatch << std::endl;
  std::cout << "LOADING AUDIO FILE: " << audioInput << std::endl;
  std::cout << "LOADING BARBERISM INSTRUCTIONS: " << controlFile << std::endl;

  // init pd
  int srate = 44100;
  //libpd_printhook = (t_libpd_printhook) pdprint;
  //libpd_noteonhook = (t_libpd_noteonhook) pdnoteon;
  libpd_init();
  libpd_init_audio(1, 2, srate);
  float inbuf[64], outbuf[128];  // one input channel, two output channels
                                 // block size 64, one tick per buffer

  // compute audio    [; pd dsp 1(
  libpd_start_message(1); // one entry in list
  libpd_add_float(1.0f);
  libpd_finish_message("pd", "dsp");

  // open patch       [; pd open file folder(
  libpd_openfile(argv[1], argv[2]);

  // now run pd for ten seconds (logical time)
  int i;
  for (i = 0; i < 10 * srate / 64; i++) {
    // fill inbuf here
    libpd_process_float(1, inbuf, outbuf);
    // use outbuf here
  }

  return 0;
}
