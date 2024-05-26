import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import './App.css';
import { toast } from 'sonner';

import { useState } from 'react';
import { Button } from './components/ui/button';

function App() {
	const [video, setVideo] = useState<File | null>(null);
	const [loading, setLoading] = useState(false);
	const [image, setImage] = useState<File | null>(null);

	function handleUpload() {
		if (video) {
			setLoading(true);
			toast.success('Uploading...', {
				duration: 3000,
				position: 'bottom-right',
			});
			const formData = new FormData();
			formData.append('video', video);

			fetch('http://localhost:5000/upload', {
				method: 'POST',
				body: formData,
			})
				.then((res) => res.json())
				.then((data) => {
					setLoading(false);
					console.log(data);
					setVideo(null);
					toast.success('Video uploaded successfully', {
						duration: 3000,
						position: 'bottom-right',
					});
				})
				.catch((err) => {
					setLoading(false);
					console.error('Error uploading file:', err);
					toast.error('Error uploading file', {
						duration: 3000,
						position: 'bottom-right',
					});
				});
		} else {
			toast.error('No video selected', {
				duration: 3000,
				position: 'bottom-right',
			});
			console.error('No video selected');
		}
	}
	function handleImage() {
		fetch('http://localhost:5000/image')
			.then((res) => res.blob())
			.then((data) => {
				setImage(data as File);
				console.log(data);
			})
			.catch((err) => {
				console.error('Error uploading file:', err);
			});
	}
	function handleReset() {
		setVideo(null);
		setImage(null);
		setLoading(false);
	}
	function downloadVideo() {
		fetch('http://localhost:5000/download')
			.then((res) => res.blob())
			.then((data) => {
				const url = window.URL.createObjectURL(data);
				const a = document.createElement;
				a.href = url;
				a.download = 'video.mp4';
				a.click();
			});
	}
	return (
		<div className='flex justify-center'>
			<div className='grid w-full max-w-sm items-center gap-1.5'>
				<Label htmlFor='video'>Upload your Video Here</Label>
				<Input
					id='video'
					type='file'
					accept='video/*'
					
					onChange={(e) => setVideo(e.target.files ? e.target.files[0] : null)}
				/>
				<div>
					<Button onClick={handleUpload}>
						{loading ? 'Uploading...' : 'Upload'}
					</Button>
					<Button onClick={handleReset}>Reset</Button>
				</div>
				<br />
				<div>
					<Button onClick={handleImage}>Get First Frame</Button>
					<Button onClick={downloadVideo}>Download Video</Button>
				</div>
				{image && (
					<img
						src={URL.createObjectURL(image)}
						alt='first frame'
						className='w-100 h-100'
					/>
				)}
			</div>
		</div>
	);
}

export default App;
