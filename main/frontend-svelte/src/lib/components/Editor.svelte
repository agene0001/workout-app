<script lang="ts">
	import { onMount, onDestroy, createEventDispatcher } from 'svelte';
	import { browser } from '$app/environment';
	import { getIdToken } from 'firebase/auth';
	import {deleteImageOnServer, uploadImage} from "$lib/utils/image.utils.js";

	// Props for the component
	export let initialData = { blocks: [] }; // Default to an empty structure
	export let placeholder = "Let's write an awesome story!";
	export let autofocus = true;
	export let readOnly = false; // New prop to toggle read-only mode
	export let minHeight = '400px'; // Customizable min-height (increased from 250px)
	export let theme = 'light'; // 'light' or 'dark'

	const dispatch = createEventDispatcher();

	let editorInstance = null;
	let editorHolderId = `editorjs-instance-${Math.random().toString(36).substring(2, 11)}`;

	// Variables for dynamically imported Editor.js and its tools
	let EditorJS;
	let AlignmentTuneTool, TextColorTool, UndoTool,IndentTuneTool;
	let Header,
		ListTool,
		Paragraph,
		Quote,
		Delimiter,
		TableTool,
		CodeTool,
		ImageTool,
		LinkTool,
		EmbedTool,
		MarkerTool,
			LayoutBlockTool;

	// async function handleImageDeletion(imageUrl) {
	// 	try {
	// 		// Extract filename. Assumes URL structure is /api/v1/blog/uploaded/files/filename.ext
	// 		const filename = imageUrl.substring(imageUrl.lastIndexOf('/') + 1);
	// 		if (!filename) {
	// 			console.warn('Could not extract filename from URL for deletion:', imageUrl);
	// 			return;
	// 		}
	//
	// 		const { getClientAuth } = await import('$lib/firebase/firebase.client.js');
	// 		const auth = getClientAuth();
	//
	// 		if (!auth.currentUser) {
	// 			console.error('User not authenticated for image deletion.');
	// 			dispatch('image-delete-error', {
	// 				filename,
	// 				message: 'User not authenticated for deletion.'
	// 			});
	// 			return;
	// 		}
	// 		const idToken = await getIdToken(auth.currentUser);
	//
	// 		const response = await fetch(`/api/v1/blog/images/delete/${filename}`, {
	// 			method: 'DELETE',
	// 			headers: {
	// 				Authorization: `Bearer ${idToken}`
	// 			}
	// 		});
	//
	// 		if (response.ok) {
	// 			console.log(`Image ${filename} deleted successfully from server.`);
	// 			dispatch('image-delete-success', { filename });
	// 		} else {
	// 			const errorText = await response.text();
	// 			console.error(
	// 				`Failed to delete image ${filename} from server:`,
	// 				response.status,
	// 				errorText
	// 			);
	// 			dispatch('image-delete-error', {
	// 				filename,
	// 				message: `Deletion failed: ${response.status} ${errorText}`
	// 			});
	// 		}
	// 	} catch (error) {
	// 		console.error('Error during image deletion request:', error);
	// 		// Attempt to get filename again for dispatch, though imageUrl might be more reliable if filename extraction failed
	// 		const fn = imageUrl.substring(imageUrl.lastIndexOf('/') + 1) || imageUrl;
	// 		dispatch('image-delete-error', {
	// 			filename: fn,
	// 			message: error.message || 'Unknown deletion error'
	// 		});
	// 	}
	// }

	onMount(async () => {
		if (browser) {
			try {
				// Dynamically import Editor.js and its tools
				// Store the actual class itself, not the module
				const EditorJSModule = await import('@editorjs/editorjs');
				EditorJS = EditorJSModule.default;

				const HeaderModule = await import('@editorjs/header');
				Header = HeaderModule.default;

				const ListToolModule = await import('@editorjs/list');
				ListTool = ListToolModule.default;

				const ParagraphModule = await import('@editorjs/paragraph');
				Paragraph = ParagraphModule.default;

				const QuoteModule = await import('@editorjs/quote');
				Quote = QuoteModule.default;

				const DelimiterModule = await import('@editorjs/delimiter');
				Delimiter = DelimiterModule.default;

				const TableToolModule = await import('@editorjs/table');
				TableTool = TableToolModule.default;

				const CodeToolModule = await import('@editorjs/code');
				CodeTool = CodeToolModule.default;

				const ImageToolModule = await import('@editorjs/image');
				ImageTool = ImageToolModule.default;

				const LinkToolModule = await import('@editorjs/link');
				LinkTool = LinkToolModule.default;

				const EmbedToolModule = await import('@editorjs/embed');
				EmbedTool = EmbedToolModule.default;

				const MarkerToolModule = await import('@editorjs/marker');
				MarkerTool = MarkerToolModule.default;

				// --- IMPORT NEW TOOLS ---
				const AlignmentTuneModule = await import('editorjs-text-alignment-blocktune');
				AlignmentTuneTool = AlignmentTuneModule.default;

				const IndentTuneModule= await import('$lib/custom-indent-tune/index.ts'); // Adjust path as needed
				 IndentTuneTool= IndentTuneModule.default // Adjust path as needed


				const TextColorPluginModule = await import('editorjs-color-picker'); // <--- Changed to direct relative path
				// When dynamically importing a CJS module, the export is usually on the .default property
				TextColorTool = TextColorPluginModule.default;
				const LayoutBlockToolModule = await import('@peppap1g/editorjs-columns');
				LayoutBlockTool = LayoutBlockToolModule.default;

				// Optional: Add a check to ensure it loaded correctly
				if (!TextColorTool || typeof TextColorTool !== 'function') {
					console.error('Failed to load TextColorTool correctly. Loaded:', TextColorPluginModule);
					// Handle the error appropriately, maybe dispatch an error event
					throw new Error('TextColorTool plugin could not be loaded.');
				}

				const UndoModule = await import('editorjs-undo');
				UndoTool = UndoModule.default;
				// --- END IMPORT NEW TOOLS ---

				// Wait a small delay to ensure DOM is ready
				setTimeout(() => {
					initEditor();
				}, 100);
			} catch (error) {
				console.error('Failed to load Editor.js or its tools:', error);
				dispatch('error', { message: 'Failed to load editor resources.' });
			}
		}
	});

	function initEditor() {
		// Verify that the DOM element exists before trying to initialize
		const holderElement = document.getElementById(editorHolderId);
		if (!EditorJS || !holderElement) {
			console.warn('EditorJS library not loaded or editor holder DOM element not found yet.');
			// Retry after a short delay if DOM element isn't ready
			setTimeout(() => {
				if (document.getElementById(editorHolderId)) {
					initEditorInternal();
				} else {
					console.error('Editor holder DOM element still not found.');
					dispatch('error', { message: 'Editor holder DOM element not found.' });
				}
			}, 100);
			return;
		}
		initEditorInternal();
	}

	function initEditorInternal() {
		try {
			// Clean up previous instance if it exists
			if (editorInstance && typeof editorInstance.destroy === 'function') {
				editorInstance.destroy();
				editorInstance = null;
			}

			// Ensure initialData has the correct structure
			const dataToLoad =
				initialData && initialData.blocks && Array.isArray(initialData.blocks)
					? initialData
					: { blocks: [] };
			const layoutColumnTools = {
				header: Header,
				// alert : Alert,
				paragraph : Paragraph,
				delimiter : Delimiter
			}

			// Create a new editor instance
			editorInstance = new EditorJS({
				holder: editorHolderId,
				autofocus: !readOnly && autofocus, // Autofocus only if not readOnly
				placeholder: placeholder,
				readOnly: readOnly,
				tools: {
					header: {
						class: Header,
						inlineToolbar: true,
						config: {
							levels: [1, 2, 3, 4, 5, 6],
							defaultLevel: 2
						},
						tunes: ['alignTune',"indentTune"] // --- ADDED INDENT TUNE ---
					},
					paragraph: {
						class: Paragraph,
						inlineToolbar: true,
						tunes: ['alignTune',"indentTune"] // --- ADDED INDENT TUNE ---
					},
					list: {
						class: ListTool,
						inlineToolbar: true
					},
					quote: {
						class: Quote,
						inlineToolbar: true,
						tunes: ['alignTune',"indentTune"] // --- ALIGN TUNE (Optional for Quote) ---
					},
					delimiter: Delimiter,
					table: {
						class: TableTool,
						inlineToolbar: true
					},
					code: CodeTool,
					linkTool: LinkTool,
					layout: {
						class: LayoutBlockTool,
						config: {
							EditorJsLibrary: EditorJS, // Pass the EditorJS class
							// Pass the tools that can be used inside columns
							tools: layoutColumnTools,
							// Optional: Default layout preset
							// defaultLayout: '2-cols-equal',
							// Optional: Available layout presets
							// layouts: [
							//    { name: '2 columns', icon: '<svg>...</svg>', layout: '2-cols-equal' },
							//    { name: '3 columns', icon: '<svg>...</svg>', layout: '3-cols-equal' }
							// ]
						},
						// You can add tunes to the layout block itself if needed
						// tunes: ['alignTune']
					},
					// --- END LAYOUT TOOL CONFIGURATION ---

					image: {
						class: ImageTool,
						config: {
							// ... (your existing image uploader config)
							uploader: {
								uploadByFile: async (file: File) => {
									// --- PASTE THE REFACTORED uploadByFile LOGIC HERE ---

									// (The async function defined above)
									// It will use the imported 'uploadImage' and the 'dispatch' from this component
									dispatch('image-upload-start', { file });
									try {
										const uploadResult = await uploadImage(file);
										if (uploadResult && uploadResult.url) {
											dispatch('image-upload-success', {
												file: { url: uploadResult.url, name: uploadResult.name },
												isTemporary: false
											});
											return {
												success: 1,
												file: { url: uploadResult.url }
											};
										} else {
											const errorMessage = 'Image upload failed from Editor. Check console.';
											dispatch('image-upload-error', { file, message: errorMessage });
											return { success: 0, file: { url: null, message: errorMessage } };
										}
									} catch (error: any) {
										console.error('Error in Editor.js uploadByFile:', error);
										const errorMessage = error.message || 'Unknown upload error in Editor.js';
										dispatch('image-upload-error', { file, message: errorMessage });
										return { success: 0, file: { url: null, message: errorMessage } };
									}
									// --- END OF PASTED LOGIC ---
								},
								uploadByUrl: (url) => {
									return Promise.resolve({
										success: 1,
										file: {
											url: url
										}
									});
								}
							}
						}
					},
					embed: EmbedTool,
					marker: MarkerTool,

					// --- NEW TOOL CONFIGURATIONS ---
					alignTune: {
						// Name this whatever you used in the 'tunes' array above
						class: AlignmentTuneTool
						// config for alignment tune if any (e.g., default alignment)
						// config: {
						//   default: "left",
						//   blocks: {
						//     header: 'center', // specific default for header
						//     list: 'left'
						//   }
						// }
					},
					indentTune: {
						class: IndentTuneTool,
						config: {
							defaultIndentSize: 24, // Indent size in pixels
							maxIndentLevel: 5 // Maximum indent level
						}
					},
					textColor: {
						class: TextColorTool,
						config: {
							colorCollections: [
								'#EC7878',
								'#9C27B0',
								'#673AB7',
								'#3F51B5',
								'#0070FF',
								'#03A9F4',
								'#00BCD4',
								'#4CAF50',
								'#8BC34A',
								'#CDDC39',
								'#FFF'
							],
							defaultColor: '#FF1300',
							type: 'text',
							customPicker: true
						}
					}
					// --- END NEW TOOL CONFIGURATIONS ---
				},
				tunes: ['indentTune', 'alignTune'],
				data: dataToLoad,
				onReady: () => {
					console.log('Editor.js instance is ready!');
					// --- INITIALIZE UNDO TOOL ---
					if (UndoTool && editorInstance) {
						new UndoTool({ editor: editorInstance });
					}
					// --- END INITIALIZE UNDO TOOL ---
					dispatch('ready', { editor: editorInstance });
				},
				onChange: (api, event) => {
					// event is a CustomEvent here
					if (!readOnly) {
						dispatch('change', { api, event });

						// Handle image deletion logic
						const eventsToProcess = Array.isArray(event) ? event : [event];
						for (const currentEvent of eventsToProcess) {
							if (
								currentEvent.type === 'block-removed' &&
								currentEvent.detail &&
								currentEvent.detail.target // target is the BlockAPI
							) {
								const removedBlockAPI = currentEvent.detail.target;
								if (removedBlockAPI.name === 'image') {
									removedBlockAPI
										.save()
										.then((savedData) => {
											let rawData = savedData.data;
											if (rawData && rawData.file && rawData.file.url) {
												const imageUrl = rawData.file.url;
												// Path confirmed from StaticContentRoutes.java
												if (imageUrl.startsWith('/api/v1/blog/uploaded/images/')) {
													deleteImageOnServer(imageUrl);
												}
											}
										})
										.catch((error) => {
											console.error('Error saving block data for deletion:', error);
										});
								}
							}
						}
					}
				}
			});
		} catch (error) {
			console.error('Error initializing Editor.js:', error);
			dispatch('error', { message: 'Failed to initialize editor.' });
		}
	}

	// Method to be called by parent to get content
	export async function getContent() {
		if (editorInstance && typeof editorInstance.save === 'function' && !readOnly) {
			try {
				const savedData = await editorInstance.save();
				return savedData;
			} catch (error) {
				console.error('Error saving content from Editor.js:', error);
				dispatch('error', { message: 'Failed to get editor content.' });
				return null;
			}
		} else if (readOnly) {
			return initialData; // Return initial data if read-only
		}
		console.warn('Editor instance not available or in read-only mode.');
		return null;
	}

	// Method to clear the editor (if not readOnly)
	export function clear() {
		if (editorInstance && typeof editorInstance.clear === 'function' && !readOnly) {
			editorInstance.clear();
			dispatch('cleared');
		}
	}

	// Method to explicitly render new data
	export function render(data) {
		if (editorInstance && typeof editorInstance.render === 'function' && data && data.blocks) {
			initialData = data; // Update internal initialData for consistency if re-rendered in readOnly
			editorInstance.render(data);
		}
	}

	// Watch for changes in readOnly to toggle read-only mode
	$: if (
		browser &&
		editorInstance &&
		editorInstance.readOnly &&
		typeof editorInstance.readOnly.toggle === 'function' &&
		readOnly !== undefined
	) {
		editorInstance.readOnly.toggle(readOnly);
	}

	// Watch for initialData changes when editor is already initialized
	$: if (browser && editorInstance && initialData && initialData.blocks) {
		// Only re-render if the editor is already mounted
		if (document.getElementById(editorHolderId) && typeof editorInstance.render === 'function') {
			editorInstance.render(initialData);
		}
	}

	onDestroy(() => {
		if (browser && editorInstance && typeof editorInstance.destroy === 'function') {
			try {
				editorInstance.destroy();
			} catch (e) {
				console.error('Error destroying editor instance:', e);
			}
			editorInstance = null;
		}
	});
</script>

<div
	id={editorHolderId}
	class="editorjs-container-wrapper {theme}"
	style="min-height: {minHeight};"
>
	{#if !editorInstance}
		<div class="editor-loading">
			<div class="loading-spinner"></div>
			<div>Loading editor...</div>
		</div>
	{/if}
</div>

<style>
	/* Styles remain the same as in your provided file */
	.editorjs-container-wrapper {
		border: 1px solid #e0e0e0;
		border-radius: 8px;
		padding: 1.5rem; /* Increased padding for more space */
		min-height: 400px; /* Default minimum height */
		position: relative;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
		transition: all 0.3s ease;
	}

	.editorjs-container-wrapper:focus-within {
		border-color: #3366ff;
		box-shadow: 0 2px 12px rgba(51, 102, 255, 0.1);
	}

	.editorjs-container-wrapper.light {
		background-color: #fff;
		color: #333;
	}

	.editorjs-container-wrapper.dark {
		background-color: #1e1e1e;
		color: #e0e0e0;
		border-color: #444;
	}

	.editor-loading {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		min-height: 200px;
		color: #888;
		font-style: italic;
	}

	.loading-spinner {
		width: 30px;
		height: 30px;
		border: 3px solid #f3f3f3;
		border-top: 3px solid #3366ff;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 10px;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	/* Global styles for EditorJS elements */
	:global(.codex-editor) {
		box-sizing: border-box;
	}

	:global(.codex-editor__redactor) {
		padding-bottom: 150px !important; /* More space at the bottom */
	}

	/*:global(.ce-toolbar__content) {*/
	/*	max-width: calc(100% - 40px); !* Ensure toolbar fits within wrapper *!*/
	/*}*/

	:global(.ce-block__content) {
		max-width: 850px; /* Wider content area */
		margin: 0 auto; /* Center the content */
	}

	:global(.ce-toolbar__actions) {
		max-width: 100%; /* Allow actions to fill the container */

	}

	/* Improve paragraph and caption styling */
	:global(.ce-paragraph) {
		font-size: 16px;
		line-height: 1.6;
		margin-bottom: 12px;
	}

	:global(.image-tool__caption .cdx-input) {
		font-size: 14px;
	}

	:global(.image-tool__caption .cdx-input[data-placeholder]::before) {
		font-style: italic;
		color: #777;
	}

	:global(.ce-paragraph[data-placeholder]:empty::before) {
		color: #aaa;
		font-style: italic;
	}

	/* Improve heading styles */
	:global(.ce-header) {
		padding: 0.5em 0;
		margin: 0;
		font-weight: 600;
	}

	/* Improve toolbar buttons */
	:global(.ce-toolbar__plus, .ce-toolbar__settings-btn) {
		color: #444;
		background: #f5f5f5;

		border-radius: 6px;
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
		transition: all 0.2s ease;
	}

	:global(.ce-toolbar__plus:hover, .ce-toolbar__settings-btn:hover) {
		background: #eaeaea;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	/* Dark theme overrides */
	:global(.dark .ce-toolbar__plus, .dark .ce-toolbar__settings-btn) {
		background: #333;
		color: #e0e0e0;
	}

	:global(.dark .ce-toolbar__plus:hover, .dark .ce-toolbar__settings-btn:hover) {
		background: #444;
	}

	:global(.dark .cdx-marker) {
		background: rgba(255, 230, 0, 0.3);
	}

	:global(.dark .ce-paragraph[data-placeholder]:empty::before) {
		color: #777;
	}

	/* Focus state for blocks */
	:global(.ce-block--selected) {
		background-color: rgba(51, 102, 255, 0.05);
		border-radius: 4px;
	}

	/* Table improvements */
	:global(.tc-table) {
		border-radius: 6px;
		overflow: hidden;
		border: 1px solid #e0e0e0;
	}

	:global(.tc-cell) {
		padding: 10px 12px;
	}

	/* Code blocks */
	:global(.ce-code__textarea) {
		font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
		font-size: 14px;
		padding: 15px;
		border-radius: 6px;
		background: #f7f7f7;
	}

	:global(.dark .ce-code__textarea) {
		background: #2a2a2a;
		color: #e0e0e0;
	}


	/*!* --- End Toolbar Popover Fixes --- *!*/
</style>
