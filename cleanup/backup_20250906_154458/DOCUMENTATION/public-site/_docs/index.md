# About PFS

This experimentation aims to provide a smart storage via a virtual file system in order analyze and decompose all information up to a semantic atomic level when possible.

On the short term it acts more like a deduplication/compression system, but the idea is to build a knowledge base of atomic content and their respective grammar in order to regenerate any stored content and even more. By builing both private and public dictionnary of concepts and grammars, it makes all aspect of common knowledge discovery easier while protecting only the non-public base of knowledge as a private semantic digest.

## So? This is just for text, right ?

No, as long as a file us structured and decomposable, it can be processed on writing to PFS and regenerated on demand. In general, files are very structurated. However, a grammar must be defined in order to process this file forward and backward. This grammar and the content discovery process needs to be coded first. 

For example, a MP4 video file is a container with metadata, potentially many audio tracks, subtitles and organized video content. This video content is using a compression scheme with standard blocks of image, key frames, redundant and moving blocks, etc. All this content may be decomposed even further up to the point where some redundant information is common with other files. That's where the fun begins. Relationships can be made on many aspects of the file and its different levels of structure. Its grammar, subgrammars and semantic content needs to be stored in a convenient manner in order to find those matches independantly of the original format and even the context. So, while waiting for this particuliar grammar, DFS will more likely behave like a deduplication storage. All stored content can be processed when a new decoder is ready. Many decoders/digesters can be made over the years to analyse the content on new perspectives. As long as an original file can be regenerated, the rest is just quality of meanings.

Text is good candidate to start the project because it is what we use to code and it makes debbuging a lot easier. Moving to other kind of content is likely to be made by synesthetic association to the existing closest textual abstract primitives. It would be probably be better to work on translated text first to make those abstract primitives even more generic. Then move to movies with multilingual subtitles and related images in motion. 

## Manual coding forever or AI driven grammar generation (compiling autoencoders) ?

A bit of both probably. This is experimental and all approaches are welcome. As a proof of comcept, the manual approach is the best to refine data structures and the foundations of the system. AI have definitely a strong role to make this project go beyond fancy compression. Any help is welcommed!

