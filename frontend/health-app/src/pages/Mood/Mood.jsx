import React,{useState} from 'react'
import "./Mood.css"
import logo from "../../assets/logo-blue.png";
import profile from "../../assets/profile.png";
import axios from 'axios';

export default function Sleep() {

    const [stress,setStress]=useState(5);
    const [mood, setMood]=useState("");
    const [events, setEvents]=useState("");



    return (
    <div className='h-screen'>
        <div className='fixed w-full flex justify-between items-center px-20 h-24' >
            <a href='/dashboard'><img src={logo} alt="" className=''/></a>
            <button className="w-auto h-12 p-3 rounded-full bg-custombluebutton"><img src={profile} alt='' className="h-full"></img></button>
        </div>
        <div className="flex flex-col justify-end items-center h-screen">
            <div className="flex flex-col h-5/6 w-3/4 rounded-t-3xl shadow-md justify-center items-center">
                <div className="text-3xl m-14 font-bold">MOOD TRACKER</div>

                <div className="text-xl mt-14 mb-8">How are you feeling today?</div>
                <div className='flex mt-0'>
                    <button className={"w-36 h-12 mx-4 rounded-sm text-white font-bold"+ (mood===1?" bg-gray":" bg-red")} onClick={()=>{setMood(1)}}>AWFUL</button>
                    <button className={"w-36 h-12 mx-4 rounded-sm text-white font-bold"+ (mood===2?" bg-gray":" bg-peach")} onClick={()=>{setMood(2)}}>BAD</button>
                    <button className={"w-36 h-12 mx-4 rounded-sm text-white font-bold"+ (mood===3?" bg-gray":" bg-bluemed")} onClick={()=>{setMood(3)}}>MEH</button>
                    <button className={"w-36 h-12 mx-4 rounded-sm text-white font-bold"+ (mood===4?" bg-gray":" bg-green")} onClick={()=>{setMood(4)}}>GOOD</button>
                    <button className={"w-36 h-12 mx-4 rounded-sm text-white font-bold"+ (mood===5?" bg-gray":" bg-blueish")} onClick={()=>{setMood(5)}}>GREAT</button>
                </div>
                
                <div className="text-xl m-14">How would you rate your stress levels? </div>
                <input type='range' min='0' max='10' defaultValue={stress} className='slider' onChange={(e)=>{setStress(e.target.value)}}></input>
                <div className='text-xl mt-8'>{stress}</div>


                <div className="text-xl m-14"> List some events that might have contributed to stress: </div>
                <textarea className='rounded-lg border-black border-2' value={events} onChange={(e)=>{setEvents(e.target.value)}} cols="40" rows="4"></textarea>

                <a href='/dashboard'>
                <button className={"w-36 h-12 mt-24 rounded-full text-white font-bold" + (mood!==""?' bg-black':' bg-gray cursor-default')} onClick={()=>{
                    if(mood!==""){
                        var bodyFormData = new FormData();
                        bodyFormData.append('score', mood);
                        bodyFormData.append('stress', stress);
                        bodyFormData.append('notes', events);
                        bodyFormData.append('userid', 1);
                        bodyFormData.append('date', "2022-02-19");
                        axios({
                            method: "post",
                            url: "http://localhost:5000/api/mood/addEntry",
                            data: bodyFormData
                        })
                            .then(response => {console.log(response)})
                            .catch(error => {console.log(error)})
                    }
                }}>SUBMIT</button></a>

            </div>
        </div>
    </div>
  )
}
