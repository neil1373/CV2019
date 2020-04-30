#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

#pragma pack(2)
typedef struct BmpFileHeader{
    uint16_t bfTybe;
    uint32_t bfSize;
    uint16_t bfReserved1;
    uint16_t bfReserved2;
    uint32_t bfOffBits;
}BmpFileHeader;

typedef struct BmpInfoHeader{
    uint32_t biSize;
    uint32_t biWidth;
    uint32_t biHeight;
    uint16_t biPlanes; 
    uint16_t biBitCount;
    uint32_t biCompression;
    uint32_t biSizeImage;
    uint32_t biXPelsPerMeter;
    uint32_t biYPelsPerMeter;
    uint32_t biClrUsed;
    uint32_t biClrImportant;
}BmpInfoHeader;
#pragma pack()

int main(int argc, char const *argv[]){
    FILE *fin = fopen("lena.bmp", "rb");
    BmpFileHeader filehead;
    BmpInfoHeader infohead;
    uint8_t palette[256][4];
    fread(&filehead, 1, sizeof(BmpFileHeader), fin);
    fread(&infohead, 1, sizeof(BmpInfoHeader), fin);
    fread(palette, 256 * 4, sizeof(uint8_t), fin);
    //file head contents
    /*printf("%d %d\n", filehead.bfTybe, filehead.bfSize);
    printf("%d %d %d\n", filehead.bfReserved1, filehead.bfReserved2, filehead.bfOffBits);*/
    //info head contents
    /*printf("%d %d %d\n", infohead.biSize, infohead.biWidth, infohead.biHeight);
    printf("%d %d %d\n", infohead.biPlanes, infohead.biBitCount, infohead.biCompression);
    printf("%d %d %d\n", infohead.biSizeImage, infohead.biXPelsPerMeter, infohead.biYPelsPerMeter);
    printf("%d %d\n", infohead.biClrUsed, infohead.biClrImportant);*/
    int height = infohead.biHeight, width = infohead.biWidth;
    uint8_t original_img[height][width];
    fread(original_img, height * width, sizeof(uint8_t), fin);
    fclose(fin);
    uint8_t upside_down_img[height][width];
    uint8_t right_side_left_img[height][width];
    uint8_t diagonally_mirrored_img[height][width];
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            upside_down_img[i][j] = original_img[height - 1 - i][j]; 
            right_side_left_img[i][j] = original_img[i][width - 1 - j];
            diagonally_mirrored_img[i][j] = original_img[j][i];
        }
    }
    FILE *fout1 = fopen("lena_upside_down.bmp", "wb");
    fwrite(&filehead, 1, sizeof(BmpFileHeader), fout1);
    fwrite(&infohead, 1, sizeof(BmpInfoHeader), fout1);
    fwrite(palette, 256 * 4, sizeof(uint8_t), fout1);
    fwrite(upside_down_img, height * width, sizeof(uint8_t), fout1);
    fclose(fout1);
    FILE *fout2 = fopen("lena_right_side_left.bmp", "wb");
    fwrite(&filehead, 1, sizeof(BmpFileHeader), fout2);
    fwrite(&infohead, 1, sizeof(BmpInfoHeader), fout2);
    fwrite(palette, 256 * 4, sizeof(uint8_t), fout2);
    fwrite(right_side_left_img, height * width, sizeof(uint8_t), fout2);
    fclose(fout2);
    FILE *fout3 = fopen("lena_diagonally_mirrored.bmp", "wb");
    fwrite(&filehead, 1, sizeof(BmpFileHeader), fout3);
    fwrite(&infohead, 1, sizeof(BmpInfoHeader), fout3);
    fwrite(palette, 256 * 4, sizeof(uint8_t), fout3);
    fwrite(diagonally_mirrored_img, height * width, sizeof(uint8_t), fout3);
    fclose(fout3);
    return 0;
}