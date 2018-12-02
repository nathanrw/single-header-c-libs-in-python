/**
 * Basic Image Format
 **/

enum bif_error {
    BIF_OK = 0,
    BIF_ERROR_UNKNOWN,
    BIF_ERROR_HORRIBLY_MANGLED
};

#define BIF_FLAG(N) (1 << (N))

#define BIF_CHECK_FLAG(VAR, FLAG) (!!(VAR & FLAG))

enum bif_flags {
    BIF_FLAG_NONE = 0,
    BIF_FLAG_WIBBLE = BIF_FLAG(0),
    BIF_FLAG_WOBBLE = BIF_FLAG(1)
};

 /* Note: not including stdint. Cffi defines these for us - if this were
 a real library we would need to do some trickery since the CDef parser
 doesn't support includes and we'd need to include stdint.h. */

struct bif_image {
    uint16_t width;
    uint16_t height;
    uint32_t* buffer; /* RGBA pixels. */
};

/**
 * Read an image from a file.
 *
 * Reading will only proceed if BIF_FLAG_WIBBLE is set.
 *
 * @param filename Path to the file to read.
 * @param flags Option flags
 * @param image Pointer to a struct that will contain the image data.
 * @return BIF_OK on success, an error code otherwise.
 * @post On success, image will contain the image data comprising width,
 *       height, and pixel data buffer. It is the responsibility of the
 *       caller to free this with bif_image_free().
 * 
 */
enum bif_error bif_image_read(
  const char* filename, 
  enum bif_flags flags, 
  struct bif_image* image
);

/**
 * Free resources for an image read with bif_image_read().
 * @param image The image to free.
 * @return BIF_OK on success, an error code otherwise.
 */
enum bif_error bif_image_free(
  struct bif_image* image
);

/**
 * Write an image to a file.
 *
 * Writing will only proceed if BIF_FLAG_WOBBLE is set.
 *
 * @param filename Path to the file to read.
 * @param flags Option flags
 * @param image Pointer to a struct that contains the image data.
 * @pre image must be properly initialised with image data.
 * @return BIF_OK on success, an error code otherwise.
 */
enum bif_error bif_image_write(
  const char* filename, 
  enum bif_flags flags, 
  struct bif_image* image
);
 
#ifdef BIF_IMPLEMENTATION

#include <stdlib.h>
#include <stdio.h>

enum bif_error bif_image_read(const char* filename, enum bif_flags flags, struct bif_image* image)
{
    FILE* file;
    uint8_t bif[4];
    size_t pixel_count;
    
    if (!filename || !*filename || !image) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (!BIF_CHECK_FLAG(flags, BIF_FLAG_WIBBLE)) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    file = fopen(filename, "rb");
    if (!file) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (fread(bif, 1, 4, file) != 4) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (bif[0] != 'B' || bif[1] != 'I' || bif[2] != 'F' || bif[3] != '\0') {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (fread(&image->width, 2, 1, file) != 1) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (fread(&image->height, 2, 1, file) != 1) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    pixel_count = image->width*image->height;
    image->buffer = malloc(pixel_count*4);
    if (!image->buffer) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (fread(image->buffer, pixel_count, 4, file) != pixel_count) {
        free(image->buffer);
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    return BIF_OK;
}

enum bif_error bif_image_free(struct bif_image* image)
{
    free(image->buffer);
    return BIF_OK;
}

enum bif_error bif_image_write(const char* filename, enum bif_flags flags, struct bif_image* image)
{
    size_t pixel_count;
    FILE* file;
    uint8_t bif[] = {'B', 'I', 'F', '\0'};
    
    if (!filename || !*filename || !image || !image->buffer) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (!BIF_CHECK_FLAG(flags, BIF_FLAG_WOBBLE)) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    pixel_count = image->width*image->height;
    if (pixel_count < 1) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    file = fopen(filename, "wb");
    if (!file) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (fwrite(bif, 1, 4, file) != 4) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (fwrite(&image->width, 2, 1, file) != 1) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (fwrite(&image->height, 2, 1, file) != 1) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    if (fwrite(image->buffer, pixel_count, 4, file) != pixel_count) {
        return BIF_ERROR_HORRIBLY_MANGLED;
    }
    return BIF_OK;
}

#endif